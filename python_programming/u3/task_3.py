import sqlite3

# Создание соединения с базой данных
conn = sqlite3.connect("music.db")

# Создание курсора для выполнения операций с базой данных
cur = conn.cursor()

# Создание таблицы tMusician
cur.execute(
    """CREATE TABLE IF NOT EXISTS tMusician (
                id INTEGER PRIMARY KEY,
                nickname TEXT,
                age INTEGER,
                gender TEXT
            )"""
)

# Создание таблицы tSongs
cur.execute(
    """CREATE TABLE IF NOT EXISTS tSongs (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                musician_id INTEGER,
                FOREIGN KEY (musician_id) REFERENCES tMusician(id)
            )"""
)

# Создание таблицы tComments
cur.execute(
    """CREATE TABLE IF NOT EXISTS tComments (
                id INTEGER PRIMARY KEY,
                comment_text TEXT,
                song_id INTEGER,
                musician_id INTEGER,
                FOREIGN KEY (song_id) REFERENCES tSongs(id),
                FOREIGN KEY (musician_id) REFERENCES tMusician(id)
            )"""
)

# Заполнение таблицы tMusician данными
musicians = [
    ("Витя", 30, "М"),
    ("Амелия", 25, "Ж"),
    ("Миша", 35, "М"),
    ("Соня", 28, "Ж"),
    ("Газиз", 32, "М"),
]

cur.executemany(
    "INSERT INTO tMusician (nickname, age, gender) VALUES (?, ?, ?)", musicians
)

# Заполнение таблицы tSongs данными
songs = [
    ("Song text_file.txt", "Description text_file.txt", 1),
    ("Song 2", "Description 2", 2),
    ("Song 3", "Description 3", 3),
    ("Song 4", "Description 4", 4),
    ("Song 5", "Description 5", 5),
]

cur.executemany(
    "INSERT INTO tSongs (title, description, musician_id) VALUES (?, ?, ?)", songs
)

# Заполнение таблицы tComments данными
comments = [
    ("Тупо кайф!", 1, 2),
    ("Класные строчки", 2, 3),
    ("Невероятное исполнение!", 3, 4),
    ("Люблю это!", 4, 5),
    ("Интересно", 5, 1),
]

cur.executemany(
    "INSERT INTO tComments (comment_text, song_id, musician_id) VALUES (?, ?, ?)",
    comments,
)

# Сохранение изменений
conn.commit()

# Выполнение запросов для выборки данных
cur.execute("SELECT * FROM tMusician")
print("fetchall() from tMusician:", cur.fetchall())

cur.execute("SELECT * FROM tSongs")
print("fetchone() from tSongs:", cur.fetchone())

cur.execute("SELECT * FROM tComments")
print("fetchmany(2) from tComments:", cur.fetchmany(2))

# Закрытие курсора и соединения
cur.close()
conn.close()
