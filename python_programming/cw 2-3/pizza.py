from abc import ABC
from db import PizzaModel, session
import time

def count_time_to_cook(f):
    def timer(self):
        time_1 = time.time()
        f(self)
        time_2 = time.time()
        print("Пицца была приготовлена за ", time_2 - time_1)

    return timer

class Logger:  # класс миксин
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")


class Pizza(ABC, Logger):

    def __init__(self, name="Pizza", dough="тонкое", sauce="томатный", cost=0):
        self.name = name
        self._dough = dough
        self._sauce = sauce
        self._cost = cost
        self._toppings = []
        self.db_entity = PizzaModel(name=self.name, dough=self._dough, sauce=self._sauce, cost=self._cost)
        session.add(self.db_entity)
        session.commit()

    def __str__(self):
        return self.name
    @property
    def dough(self):
        return self._dough

    @property
    def sauce(self):
        return self._sauce

    @property
    def cost(self):
        return self._cost

    def prepare_dough(self):
        self.log("Замешиваем тесто...")

    def add_sauce(self):
        self.log("Добавляем соус...")

    def add_toppings(self):
        self.log("Добавляем топпинги:" + str(self._toppings))

    def bake(self):
        self.log("Выпекаем пиццу...")

    def cut(self):
        self.log("Режем пиццу...")

    def pack(self):
        self.log("Упаковываем пиццу...")

    @count_time_to_cook
    def make_pizza(self):
        self.prepare_dough()
        self.add_sauce()
        self.add_toppings()
        self.bake()
        self.cut()
        self.pack()

    def __eq__(self, other):
        if isinstance(other, Pizza):
            return (self.dough, self.sauce, self.cost) == (
                other.dough,
                other.sauce,
                other.cost,
            )
        return False

    # Перегрузка оператора сложения (+)
    def __add__(self, other):
        if isinstance(other, Pizza):
            total_cost = self.cost + other.cost
            return Pizza(cost=total_cost)
        else:
            raise TypeError(
                "Неподдерживаемые операнды для +: '{}' and '{}'".format(
                    type(self).__name__, type(other).__name__
                )
            )


class PepperoniPizza(Pizza):
    def __init__(self, dough="тонкое", sauce="томатный"):
        super().__init__("Pepperoni", dough, sauce, 10)
        self._toppings = ["пепперони", "сыр", "перец"]


class BBQPizza(Pizza):
    def __init__(self, dough="толстое", sauce="барбекю"):
        super().__init__("BBQPizza", dough, sauce, 20)
        self._toppings = ["курица", "бекон", "сыр", "лук"]


class SeafoodPizza(Pizza):
    def __init__(self, dough="тонкое", sauce="сливочный"):
        super().__init__("SeafoodPizza", dough, sauce, 40)
        self._toppings = ["морепродукты", "сыр", "оливки", "лук"]
