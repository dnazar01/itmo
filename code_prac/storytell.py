
from datetime import timedelta
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Union
import pandas as pd
from tqdm.auto import tqdm

# ─────────────────────────── 1. Константы ────────────────────────────
RU_MONTH: Dict[int, str] = {
    1: "января", 2: "февраля", 3: "марта",   4: "апреля",
    5: "мая",    6: "июня",    7: "июля",    8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря",
}

LABEL_MAP: Dict[str, str] = {
    "label_waiting_client":          "ожидаем клиента",
    "label_waiting_inside_company":  "ожидаем внутри компании",
    "label_waiting_backoffice":      "ожидаем бэк-офис",
    "label_waiting_partner":         "ожидаем партнёра",
    "label_waiting_external_org":    "ожидаем внешнюю организацию",
    "label_waiting_incident":        "ожидаем устранения инцидента",
}

CONSULT_MAP: Dict[str, str] = {
    "Auto.ConsiderationOfClaim.Result":        "сообщили результат",
    "Auto.ConsiderationOfClaim.PriorityBoost": "эскалировали",
    "Auto.ConsiderationOfClaim.NotExpired":    "сообщили срок рассмотрения",
    "Auto.ConsiderationOfClaim.DopInfo":       "добавили информацию (доп инфо)",
    "Auto.ConsiderationOfClaim.ObtainDocument":"прикрепили документы",
    "Member.IncreasePrior.FirstAppeal":        "эскалировали",
    "Member.IncreasePrior.RSV":                "РСВ",
}

# читаемые причины эскалации
ESC_REASON = {
    None:                                        "нужно решить обращение быстрее",
    "Не определено":                            "нужно решить обращение быстрее",
    "Клиент настаивает на ускорении":           "нужно решить обращение быстрее",
    "Клиент настаивает на ускорении + угрозы":  "нужно решить обращение быстрее и при этом угрожал",
    "У клиента критическая ситуация":           "у него критическая ситуация и обращение нужно решить быстрее",
    "У клиента критическая ситуация + угрозы":  "у него критическая ситуация, при этом он угрожал",
}
def _esc_text(cat: Optional[str]) -> str:
    return ESC_REASON.get(cat, str(cat).lower())

# ───────────────────── 2. Форматеры ─────────────────────
def _plural(n: int, forms: Tuple[str, str, str]) -> str:
    if n % 10 == 1 and n % 100 != 11:
        f = forms[0]
    elif 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        f = forms[1]
    else:
        f = forms[2]
    return f"{n} {f}"

def _fmt_dt(ts: pd.Timestamp) -> str:
    return f"{ts.day} {RU_MONTH[ts.month]} {ts:%H:%M}"

def _fmt_td(td: timedelta) -> str:
    sec = int(td.total_seconds())
    d, sec = divmod(sec, 86_400)
    h, sec = divmod(sec, 3_600)
    m, _   = divmod(sec,   60)
    parts: List[str] = []
    if d: parts.append(_plural(d, ("день", "дня", "дней")))
    if h: parts.append(_plural(h, ("час", "часа", "часов")))
    if m or not parts: parts.append(_plural(m, ("минута", "минуты", "минут")))
    return " ".join(parts)

def _prefix(label: Optional[str]) -> str:
    return "в чате " if label == "чат" else "во время звонка " if label == "звонок" else ""

# ─────────────────── 3. Story-builder ───────────────────
def build_story(data: Union[pd.DataFrame, str, Path], *, tz: Optional[str] = None) -> str:
    # 3.1 загрузка -----------------------------------------------------
    if isinstance(data, (str, Path)):
        p = Path(data)
        if not p.exists():
            raise FileNotFoundError(p)
        df = (pd.read_parquet if p.suffix == ".parquet" else pd.read_csv)(p)
    else:
        df = data.copy()

    # 3.2 пред-обработка ----------------------------------------------
    df["dttm"] = pd.to_datetime(df["dttm"])
    for col in ("call_end_dttm", "chat_end_dttm", "due_dttm"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    if tz:
        df["dttm"] = df["dttm"].dt.tz_localize(tz, nonexistent="shift_forward")

    df = df[~df["event_type"].str.startswith("csat")]                # убираем CSAT
    df["__ord"] = df["event_type"].map({"task_opened": 0, "deadline_set": 1}).fillna(2)
    df = df.sort_values(["dttm", "__ord"]).drop(columns="__ord").reset_index(drop=True)

    # 3.3 runtime-переменные ------------------------------------------
    active: List[Tuple[str, Optional[pd.Timestamp], str]] = []        # kind,end,label
    started_call = started_chat = None
    task_open_times: Dict[str, pd.Timestamp] = {}
    story: List[str] = []
    prev_row = None
    last_date: Optional[pd.Timestamp.date] = None

    # 3.4 основной цикл -----------------------------------------------
    for r in df.itertuples(index=False):
        now = r.dttm

        # ── сначала закрываем интервалы (чат / звонок) ──
        still = []
        for kind, end, label in active:
            if end is not None and now >= end:
                dur = _fmt_td(end - (started_call if kind == "call" else started_chat))
                story.append(f"{_fmt_dt(end)} {label} завершён, длился {dur}.")
            else:
                still.append((kind, end, label))
        active = still

        # ── если наступил новый день — вставляем три пустых строки ──
        if last_date is not None and now.date() != last_date and story:
            story.extend(["", "", ""])
        last_date = now.date()

        et = r.event_type

        # ── начало call/chat ──
        if et in ("incoming_call", "outgoing_call"):
            label = "звонок"
            phrase = "клиент позвонил нам" if et == "incoming_call" else "мы позвонили клиенту"
            story.append(f"{_fmt_dt(now)} {phrase}.")
            end = getattr(r, "call_end_dttm", None)
            if pd.isna(end) and pd.notna(getattr(r, "call_duration", None)):
                end = now + pd.to_timedelta(r.call_duration)
            active.append(("call", end, label))
            started_call = now
            prev_row = r
            continue

        if et == "chat":
            label = "чат"
            story.append(f"{_fmt_dt(now)} клиент начал чат.")
            end = getattr(r, "chat_end_dttm", None)
            if pd.isna(end) and pd.notna(getattr(r, "chat_duration", None)):
                end = now + pd.to_timedelta(r.chat_duration)
            active.append(("chat", end, label))
            started_chat = now
            prev_row = r
            continue

        inside = active[-1][2] if active else None
        pref = _prefix(inside)

        # ── task open / close ──
        if et == "task_opened":
            tn = getattr(r, "crm_task_no", None) or r.task_id
            rep = "повторное " if int(getattr(r, "task_at_problem_number", 1)) > 1 else ""
            story.append(f"{_fmt_dt(now)} зарегистрировали {rep}обращение {tn}.")
            task_open_times[r.task_id] = now
            prev_row = r
            continue

        if et == "task_closed":
            open_time = task_open_times.get(r.task_id)
            if open_time:
                story.append(f"{_fmt_dt(now)} обращение {getattr(r,'crm_task_no', r.task_id)} закрыто, "
                             f"над ним работали {_fmt_td(now - open_time)}.")
            else:
                story.append(f"{_fmt_dt(now)} обращение закрыто.")
            prev_row = r
            continue

        # ── deadline ──
        if et == "deadline_set":
            due = _fmt_dt(r.due_dttm)
            if int(getattr(r, "deadline_number", 1)) == 1:
                phrase = f"{pref}{_fmt_dt(now)} мы сказали клиенту, что решим его обращение до {due}."
            else:
                phrase = f"{pref}{_fmt_dt(now)} мы перенесли срок на {due}."
            story.append(phrase)
            prev_row = r
            continue

        # ── note ──
        if et == "note":
            raw_txt = str(getattr(r, "note_txt", "")).strip()
            if not raw_txt:
                txt = "без текста"
            elif len(raw_txt) > 120:
                txt = raw_txt[:117].rstrip() + "  ..."
            else:
                txt = raw_txt
            story.append(f"{pref}{_fmt_dt(now)} мы написали клиенту: «{txt}».")
            prev_row = r
            continue

        # ── consultation ──
        if et == "consultation":
            code = getattr(r, "consultation_code", None) \
                   or getattr(r, "consultation_result", None) or ""
            if code not in {
                    "Auto.ConsiderationOfClaim.Result",
                    "Auto.ConsiderationOfClaim.NotExpired",
                    "Auto.ConsiderationOfClaim.DopInfo",
                    "Auto.ConsiderationOfClaim.ObtainDocument",
                    "Member.IncreasePrior.RSV"
                }:
                    prev_row = r
                    continue                # ← пропускаем такие консультации

            action = CONSULT_MAP.get(code, code) or "консультация"
            story.append(f"{pref}{_fmt_dt(now)} {action}.")
            prev_row = r
            continue

        # ── escalation ──
        if et == "escalation":
            cat = getattr(r, "escalation_category", None)
            phrase = (f"{pref}{_fmt_dt(now)} клиент настаивал на том, что {_esc_text(cat)} "
                      f"(эскалировал обращение).")
            if prev_row is not None and prev_row.event_type == "consultation" and prev_row.dttm == r.dttm:
                if story:
                    story.pop()                             # убираем консультацию
            story.append(phrase)
            prev_row = r
            continue

        # ── label ──  (теперь просто игнорируем)
        if et in LABEL_MAP:
            prev_row = r               # фиксируем, но **не пишем** в story
            continue

        prev_row = r   # неизвестный тип события

    # 3.5 закрываем висящие call/chat ---------------------------------
    for kind, end, label in active:
        if end is None:
            continue
        dur = _fmt_td(end - (started_call if kind == "call" else started_chat))
        story.append(f"{_fmt_dt(end)} {label} завершён, длился {dur}.")

    return "\n".join(story)

def load_data_from_excel(file_path: Union[str, Path]) -> pd.DataFrame:
    """Загружает данные из Excel-файла в DataFrame."""
    df = pd.read_excel(file_path)

    # Явно преобразуем нужные столбцы в строку, чтобы избежать .0
    for col in ["crm_task_no"]:
        if col in df.columns:
            df[col] = df[col].astype("Int64").astype(str).replace("<NA>", pd.NA).fillna("")

    return df

def save_stories_to_excel(df: pd.DataFrame, output_path: Union[str, Path]):
    """Сохраняет DataFrame с историями в Excel-файл."""
    df.to_excel(output_path, index=False)
    print(f"Сторителлинг сохранён в {output_path}")

def generate_stories_from_excel(input_file: Union[str, Path], output_file: Union[str, Path]):
    # Загружаем и сортируем
    df = load_data_from_excel(input_file)
    df = df.sort_values(by=["first_task_id", "dttm"]).reset_index(drop=True)
    assert df["first_task_id"].is_monotonic_increasing, "first_task_id должен быть отсортирован"
    # Группируем
    grouped = df.groupby("first_task_id", sort=False)

    # Строим сторителлинги
    stories = []
    for task_id, group in tqdm(grouped, total=len(grouped), desc="stories"):
        story = build_story(group)
        stories.append({"first_task_id": task_id, "story": story})

    result_df = pd.DataFrame(stories)
    save_stories_to_excel(result_df, output_file)

# Пример использования
input_file = "/storytell/v2/our_v3 - 15к и 1806 уник проблемы/17317720_10#problem__marked_efforts_stories.xlsx"
output_file = "/storytell/v2/our_v3 - 15к и 1806 уник проблемы/out_17317720_10#problem__marked_efforts_stories.xlsx"
generate_stories_from_excel(input_file, output_file)
