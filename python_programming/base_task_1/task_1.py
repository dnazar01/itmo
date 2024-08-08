from abc import ABC
import time


# метакласс позволит выводит сообщения о том, что класс был создан/удален/изменен
# позволяет регистрировать классы


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
    def __init__(self, dough="тонкое", sauce="томатный", cost=0):
        self._dough = dough
        self._sauce = sauce
        self._cost = cost

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
        raise NotImplementedError("Метод должен быть реализован в дочерних классах.")

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
        super().__init__(dough, sauce, 10)
        self._toppings = ["пепперони", "сыр", "перец"]

    def add_toppings(self):
        print("Добавляем топпинги:", ", ".join(self._toppings))


class BBQPizza(Pizza):
    def __init__(self, dough="толстое", sauce="барбекю"):
        super().__init__(dough, sauce, 20)
        self._toppings = ["курица", "бекон", "сыр", "лук"]

    def add_toppings(self):
        print("Добавляем топпинги:", ", ".join(self._toppings))


class SeafoodPizza(Pizza):
    def __init__(self, dough="тонкое", sauce="сливочный"):
        super().__init__(dough, sauce)
        self._toppings = ["морепродукты", "сыр", "оливки", "лук"]

    def add_toppings(self):
        print("Добавляем топпинги:", ", ".join(self._toppings))


class Order:
    def __init__(self):
        self._pizzas = []

    def add_pizza(self, pizza):
        self._pizzas.append(pizza)

    def calculate_total(self):
        total_cost = 0
        for pizza in self._pizzas:
            total_cost += pizza.cost
        return total_cost


class Terminal:
    def __init__(self):
        self.database = {1: 10, 2: 20, 3: 30}
        self.order = None

    def display_menu(self):
        print("Меню:")
        print("text_file.txt. Пепперони пицца")
        print("2. Барбекю пицца")
        print("3. Дары моря пицца")

    def take_order(self):
        order = Order()
        while True:
            self.display_menu()
            choice = input(
                "Выберите пиццу по номеру (или 'закончить' для завершения заказа): "
            )
            if choice.lower() == "закончить":
                break
            elif choice in ["text_file.txt", "2", "3"]:
                quantity = int(input("Введите количество: "))
                if quantity > self.database[int(choice)]:
                    print(
                        "Некорректный ввод. На кухне нет такого количества пицц данного вида"
                    )
                else:
                    self.database[int(choice)] -= quantity
                    for i in range(quantity):
                        if choice == "text_file.txt":
                            pizza = PepperoniPizza()
                            order.add_pizza(pizza)
                        if choice == "2":
                            pizza = BBQPizza()
                            order.add_pizza(pizza)
                        if choice == "3":
                            pizza = SeafoodPizza()
                            order.add_pizza(pizza)
            else:
                print(
                    "Некорректный ввод. Пожалуйста, выберите номер из меню или введите 'закончить'."
                )
            self.order = order
        return order

    def confirm_order(self):
        if not self.order:
            print("Заказ не был сделан.")
        else:
            print("Ваш заказ:")
            for pizza, quantity in self.order.items():
                print(f"{pizza}: {quantity}")
            confirm = input("Подтвердите заказ (да/нет): ")
            if confirm.lower() == "да":
                print("Заказ подтвержден.")
            else:
                print("Заказ отменен.")


pepperoni = PepperoniPizza()
pepperoni.make_pizza()
