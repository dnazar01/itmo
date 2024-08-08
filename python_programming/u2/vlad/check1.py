from random import randint
from abc import ABC, abstractmethod
import time
import asyncio
import sqlite3


def time_of_function(func):
    def timer(*args):
        start_time = time.perf_counter_ns()
        res = func(*args)
        print(
            "Время выполнения функции",
            func.__name__,
            (time.perf_counter_ns() - start_time) / 10000,
            "секунд",
        )
        return res

    return timer


async def waiting():
    print("Идет подготовка бойцов...")
    await asyncio.sleep(2)
    print("Бойцы размялись успешно!")
    await asyncio.sleep(1)
    print("Бойцы начали драться!")


def second_fight():
    print("Вторичный поток")
    asyncio.run(waiting())
    Duel(input("Введите нужный поединок:")).fight()


class Health(ABC):
    def __init__(self, health):
        self._health = health

    @property
    def health(self):
        return self._health


class Fighter(ABC):
    connection = sqlite3.connect("fighters.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Fighters ("
        "name TEXT, "
        "health INT,"
        "power INT,"
        "stun INT"
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

    def __add__(self, value=20):
        return Fighter(self.name, self.health.health + value)

    def __sub__(self, value=20):
        return Fighter(self.name, self.health.health - value)


class Cats(Fighter):
    def __init__(self, name="", health=100, stun=randint(1, 10)):
        Fighter.__init__(self, name, health, stun)

    @time_of_function
    def __add__(self, value=20):
        return Cats(self.name, self._health.health + value)

    @time_of_function
    def __sub__(self, value=20):
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
    def __add__(self, value=20):
        return Dogs(self.name, self._health.health + value)

    @time_of_function
    def __sub__(self, value=20):
        return Dogs(self.name, self._health.health - value)

    def block(self):
        print(f"{self.name} успел защититься!")


class End_fight(Cats, Dogs):
    @staticmethod
    def ending():
        if randint(1, 2) == 1:
            return print(
                "После драки отправились в бар отдохнуть, уважение такому поступку!"
            )
        else:
            return print("После драки рябатя обиделись и больше никогда не виделись!")


class ValueOutOfRangeError(Exception):
    pass


class Duel:
    def __init__(self, count):
        self.count = count
        if count == "text_file.txt":
            name_1 = input("Введите имя первого кота\n")
            arr = (f"Кот {name_1}", 100, 20, Cats.bonus_stun())
            Fighter.cursor.executemany(
                "INSERT INTO Fighters VALUES(?, ?, ?, ?);", (arr,)
            )
            Fighter.connection.commit()
            self.first = Cats(name_1, 100)
            name_2 = input("Введите имя второго кота\n")
            arr = (f"Кот {name_2}", 100, 20, Cats.bonus_stun())
            Fighter.cursor.executemany(
                "INSERT INTO Fighters VALUES(?, ?, ?, ?);", (arr,)
            )
            Fighter.connection.commit()
            self.second = Cats(name_2, 100)
        elif count == "2":
            name = input("Введите имя первой собаки\n")
            arr = (f"Кот {name}", 100, 20, Dogs.pretend_to_be_dead())
            Fighter.cursor.executemany(
                "INSERT INTO Fighters VALUES(?, ?, ?, ?);", (arr,)
            )
            Fighter.connection.commit()
            self.first = Dogs(name, 100)
            name = input("Введите имя второй собаки\n")
            arr = (f"Кот {name}", 100, 20, Dogs.pretend_to_be_dead())
            Fighter.cursor.executemany(
                "INSERT INTO Fighters VALUES(?, ?, ?, ?);", (arr,)
            )
            Fighter.connection.commit()
            self.second = Dogs(name, 100)
        elif count == "3":
            name_1 = input("Введите имя кота\n")
            arr = (f"Кот {name_1}", 100, 20, Cats.bonus_stun())
            Fighter.cursor.executemany(
                "INSERT INTO Fighters VALUES(?, ?, ?, ?);", (arr,)
            )
            Fighter.connection.commit()
            self.first = Cats(name_1, 100)
            name_2 = input("Введите имя собаки\n")
            arr = (f"Кот {name_2}", 100, 20, Dogs.pretend_to_be_dead())
            Fighter.cursor.executemany(
                "INSERT INTO Fighters VALUES(?, ?, ?, ?);", (arr,)
            )
            Fighter.connection.commit()
            self.second = Dogs(name_2, 100)

    def fight(self):
        count_hit = 0
        while True:
            shoot = randint(1, 2)
            if not Dogs().pretend_to_be_dead() and not Cats().bonus_stun():
                if shoot == 1:
                    print("Атаковал первый")
                    self.second = self.second.__sub__(20)
                    print(
                        f"Здоровье первого = {self.first.get_health()}\nЗдоровье второго = {self.second.get_health()}"
                    )
                    count_hit += 1
                else:
                    print("Атаковал второй")
                    self.first = self.first.__sub__(20)
                    print(
                        f"Здоровье первого = {self.first.get_health()}\nЗдоровье второго = {self.second.get_health()}"
                    )
                    count_hit += 1
                if self.first.get_health() == 0:
                    print(f"Победил второй")
                    break
                elif self.second.get_health() == 0:
                    print("Победил первый")
                    break
            else:
                if Dogs().pretend_to_be_dead():
                    print('Успешно проведен прием "притвориться мертвым"')
                    print(
                        f"Здоровье первого = {self.first.get_health()}\nЗдоровье второго = {self.second.get_health()}"
                    )
                else:
                    print("Противник обездвижен")
                    print(
                        f"Здоровье первого = {self.first.get_health()}\nЗдоровье второго = {self.second.get_health()}"
                    )
            next_step = 1
            while next_step:
                next_step = input("Чтобы продолжить нажмите Enter: ")
                format(next_step)
