# Создание графического интерфейса с помощью tkinter

from random import randint
from abc import ABC, abstractmethod
import time
import asyncio
import sqlite3
from tkinter import *
from tkinter import ttk

# Создание окна и задание заголовка и размеров
window = Tk()
window.title("Бойцовский клуб")
window.geometry("800x600")


# Определение функции для кнопки выхода
def ex():
    exit()


# Очистка фрейма от виджетов
def frame_clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# Декоратор для измерения времени выполнения функции
def time_of_function(func):
    def timer(*args):
        start_time = time.perf_counter_ns()
        res = func(*args)
        ttk.Label(
            window,
            text=f"Время выполнения функции {func.__name__}: {(time.perf_counter_ns() - start_time)/10000} секунд",
        ).pack()
        return res

    return timer


# Асинхронная функция для анимации ожидания
async def waiting():
    frame_clear(window)
    ttk.Label(window, text=f"Идет подготовка бойцов...").pack()
    await asyncio.sleep(2)
    ttk.Label(window, text=f"Бойцы размялись успешно!").pack()
    await asyncio.sleep(1)
    ttk.Label(window, text=f"Бойцы начали драться!").pack()


# Функция для запуска вторичного потока
def second_fight():
    # Отображение информации о вторичном потоке
    ttk.Label(window, text=f"Вторичный поток").pack()
    # Запуск функции анимации ожидания в асинхронном режиме
    asyncio.run(waiting())
    # Запуск дуэли
    Duel(input("Введите нужный поединок:")).fight()


# Создание кнопки выхода
exit_button = ttk.Button(window, text="Выход", command=ex)
exit_button.pack(side=BOTTOM)

# Создание заголовка главного меню
main_title = ttk.Label(window, text="Выберите нужный раздел")
main_title.pack(side=TOP)

# Создание фрейма для раздела с бойцами
fighters_frame = Frame(window)
fighters_frame.pack(side=LEFT)

# Создание заголовка для раздела с бойцами
fighters_title = ttk.Label(fighters_frame, text="Список бойцов")
fighters_title.pack()


# Определение класса для представления здоровья бойца
class Health(ABC):
    def __init__(self, health):
        self._health = health

    @property
    def health(self):
        return self._health


# Определение абстрактного класса для бойцов
class Fighter(ABC):
    connection = sqlite3.connect("fighters.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Fighters ("
        "name TEXT, "
        "health INT,"
        "power INT,"
        "stun INT,"
        "count_hit INT);"
    )
    connection.commit()

    def __init__(self, name="", health=100, power=0, stun=randint(1, 10), count_hit=0):
        self._name = name
        self._health = Health(health)
        self._power = power
        self._stun = stun
        self.count_hit = count_hit

    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    @abstractmethod
    def block(self):
        pass

    def hit(self):
        return self.count_hit

    def get_power(self):
        return self._power

    def get_stun(self):
        return self._stun

    def add(self, value=20):
        return Fighter(self.name, self.health.health + value)

    def sub(self, value=20):
        return Fighter(self.name, self.health.health - value)


# Определение класса для котов
class Cats(Fighter):
    def __init__(self, name="", health=100, stun=randint(1, 10)):
        Fighter.__init__(self, name, health, stun)

    @time_of_function
    def add(self, value=20):
        return Cats(self.name, self._health.health + value)

    @time_of_function
    def sub(self, value=20):
        return Cats(self.name, self._health.health - value)

    def get_health(self):
        return self.health.health

    def get_name(self):
        return self.name

    @staticmethod
    def bonus_stun():
        if randint(1, 10) == 5:
            return True
        else:
            return False

    def block(self):
        print(f"{self.name} успел защититься!")


# Определение класса для собак
class Dogs(Fighter):
    def __init__(self, name="", health=100, died=randint(1, 10)):
        Fighter.__init__(self, name, health, died)

    def get_health(self):
        return self.health.health

    def get_name(self):
        return self.name

    @staticmethod
    def pretend_to_be_dead():
        if randint(1, 10) == 5:
            return True
        else:
            return False

    @time_of_function
    def add(self, value=20):
        return Dogs(self.name, self._health.health + value)

    @time_of_function
    def sub(self, value=20):
        return Dogs(self.name, self._health.health - value)

    def block(self):
        print(f"{self.name} успел защититься!")


# Определение класса для окончания драки
class End_fight(Cats, Dogs):
    @staticmethod
    def ending():
        if randint(1, 2) == 1:
            ttk.Label(
                window,
                text=f"После драки отправились в бар отдохнуть, уважение такому поступку!",
            ).pack()
        else:
            ttk.Label(
                window,
                text=f"После драки рябатя обиделись и больше никогда не виделись!",
            ).pack()


def add_cat():
    connection = sqlite3.connect("fighters.db")
    cursor = connection.cursor()
    values = [
        ("Мурзик", 100, 10, 5, 0),
        ("Барсик", 90, 15, 6, 0),
        ("Рыжик", 80, 20, 7, 0),
    ]
    cursor.execute(
        "INSERT INTO Fighters (name, health, power, stun, count_hit) "
        "VALUES (?, ?, ?, ?, 0)",
        values,
    )
    connection.commit()
    connection.close()


def add_dog():
    connection = sqlite3.connect("fighters.db")
    cursor = connection.cursor()
    values = [("Рэкс", 110, 12, 4, 0), ("Тузик", 95, 17, 5, 0), ("Шарик", 85, 22, 6, 0)]
    cursor.execute(
        "INSERT INTO Fighters (name, health, power, stun, count_hit) "
        "VALUES (?, ?, ?, ?, 0)",
        values,
    )
    connection.commit()
    connection.close()


# Создание кнопки для выбора котов
cats_button = ttk.Button(
    fighters_frame,
    text="Коты",
    command=lambda: frame_clear(fighters_frame)
    or ttk.Label(
        fighters_frame,
        text="Список котов",
    ).pack(),
)
cats_button.pack()

# Создание кнопки для выбора собак
dogs_button = ttk.Button(
    fighters_frame,
    text="Собаки",
    command=lambda: frame_clear(fighters_frame)
    or ttk.Label(fighters_frame, text="Список собак").pack(),
)
dogs_button.pack()

# Создание фрейма для раздела с дуэлями
duels_frame = Frame(window)
duels_frame.pack(side=RIGHT)

# Создание заголовка для раздела с дуэлями
duels_title = ttk.Label(duels_frame, text="Раздел с дуэлями")
duels_title.pack()


# Определение функции для дуэлей
class Duel:
    def __init__(self, fighter1, fighter2):
        self._fighter1 = fighter1
        self._fighter2 = fighter2

    def fight(self):
        fighter1 = self._fighter1
        fighter2 = self._fighter2
        first_hit = randint(1, 2)
        count_hit1 = 0
        count_hit2 = 0
        if first_hit == 1:
            ttk.Label(window, text=f"{fighter1.name} бьет первым!").pack()
        else:
            ttk.Label(window, text=f"{fighter2.name} бьет первым!").pack()
        while True:
            if first_hit == 1:
                count_hit1 += 1
                ttk.Label(
                    window, text=f"{fighter1.name} ударил {fighter2.name}!"
                ).pack()
                if fighter2.block():
                    first_hit = 2
                    continue
                fighter2.sub(fighter1.get_power())
                if fighter2.get_health() <= 0:
                    End_fight.ending()
                    break
                if Cats.bonus_stun():
                    ttk.Label(
                        window, text=f"{fighter1.name} оглушает {fighter2.name}!"
                    ).pack()
                    first_hit = 1
                    continue
                ttk.Label(
                    window, text=f"{fighter2.name} атакует {fighter1.name}!"
                ).pack()
                if fighter1.block():
                    first_hit = 1
                    continue
                fighter1.sub(fighter2.get_power())
                if fighter1.get_health() <= 0:
                    End_fight.ending()
                    break
                if Dogs.pretend_to_be_dead():
                    ttk.Label(
                        window, text=f"{fighter2.name} притворяется мертвым!"
                    ).pack()
                    break
                first_hit = 1
            else:
                count_hit2 += 1
                ttk.Label(
                    window, text=f"{fighter2.name} ударил {fighter1.name}!"
                ).pack()
                if fighter1.block():
                    first_hit = 1
                    continue
                fighter1.sub(fighter2.get_power())
                if fighter1.get_health() <= 0:
                    End_fight.ending()
                    break
                if Dogs.pretend_to_be_dead():
                    ttk.Label(
                        window, text=f"{fighter2.name} притворяется мертвым!"
                    ).pack()
                    break
                if Cats.bonus_stun():
                    ttk.Label(
                        window, text=f"{fighter2.name} оглушает {fighter1.name}!"
                    ).pack()
                    first_hit = 2
                    continue
                ttk.Label(
                    window, text=f"{fighter1.name} атакует {fighter2.name}!"
                ).pack()
                if fighter2.block():
                    first_hit = 2
                    continue
                fighter2.sub(fighter1.get_power())
                if fighter2.get_health() <= 0:
                    End_fight.ending()
                    break
                first_hit = 2
                if count_hit1 >= 10 and count_hit2 >= 10:
                    ttk.Label(window, text=f"У бойцов закончилась выносливость!").pack()
                    break

            # Создание кнопки для запуска дуэли в главном меню


duel_button = ttk.Button(window, text="Дуэль", command=second_fight)
duel_button.pack(side=BOTTOM)
"""INSERT INTO Fighters(name, health, power, stun, count_hit) VALUES ('Мурзик', 100, 10, 5, 0);
INSERT INTO Fighters(name, health, power, stun, count_hit) VALUES ('Барсик', 90, 15, 6, 0);
INSERT INTO Fighters(name, health, power, stun, count_hit) VALUES ('Рыжик', 80, 20, 7, 0);

INSERT INTO Fighters(name, health, power, stun, count_hit) VALUES ('Рэкс', 110, 12, 4, 0);
INSERT INTO Fighters(name, health, power, stun, count_hit) VALUES ('Тузик', 95, 17, 5, 0);
INSERT INTO Fighters(name, health, power, stun, count_hit) VALUES ('Шарик', 85, 22, 6, 0);
"""
# Открытие окна
window.mainloop()
