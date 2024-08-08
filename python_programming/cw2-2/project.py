from abc import ABC
import time, asyncio, sqlite3
from exceptions import IncorrectInputError, OutOfStockError, EmptyOrderError


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
        self._toppings = []

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
        super().__init__(dough, sauce, 10)
        self._toppings = ["пепперони", "сыр", "перец"]


class BBQPizza(Pizza):
    def __init__(self, dough="толстое", sauce="барбекю"):
        super().__init__(dough, sauce, 20)
        self._toppings = ["курица", "бекон", "сыр", "лук"]


class SeafoodPizza(Pizza):
    def __init__(self, dough="тонкое", sauce="сливочный"):
        super().__init__(dough, sauce, 40)
        self._toppings = ["морепродукты", "сыр", "оливки", "лук"]


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

    # Метод для получения списка пицц в заказе
    def get_pizzas(self):
        return self._pizzas


class Terminal:
    def __init__(self):
        # Connect to the SQLite database
        self.conn = sqlite3.connect("pizza.db")
        self.cursor = self.conn.cursor()

        # Create a table if it doesn't exist
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pizzas (
                id INTEGER PRIMARY KEY,
                name TEXT,
                quantity INTEGER
            )
        """
        )
        self.conn.commit()

        # Insert initial pizza quantities
        self.cursor.executemany(
            """
            INSERT INTO pizzas (name, quantity) VALUES (?, ?)
        """,
            [("Пепперони пицца", 10), ("Барбекю пицца", 20), ("Дары моря пицца", 30)],
        )
        self.conn.commit()

        self.order = None

    def take_order(self):
        order = Order()
        while True:
            self.display_menu()
            choice = input(
                "Выберите пиццу по номеру (или 'закончить' для завершения заказа): "
            )
            if choice.lower() == "закончить":
                break
            elif choice in ["1", "2", "3"]:
                try:
                    quantity = int(input("Введите количество: "))
                    if quantity < 1:
                        raise IncorrectInputError
                    # Check quantity from the database
                    self.cursor.execute(
                        "SELECT quantity FROM pizzas WHERE id = ?", (int(choice),)
                    )
                    available_quantity = self.cursor.fetchone()[0]
                    if quantity > available_quantity:
                        raise OutOfStockError(f"Пиццы {choice}")
                    else:
                        # Update quantity in the database
                        remaining_quantity = available_quantity - quantity
                        self.cursor.execute(
                            "UPDATE pizzas SET quantity = ? WHERE id = ?",
                            (remaining_quantity, int(choice)),
                        )
                        self.conn.commit()
                        for i in range(quantity):
                            if choice == "1":
                                pizza = PepperoniPizza()
                                order.add_pizza(pizza)
                            if choice == "2":
                                pizza = BBQPizza()
                                order.add_pizza(pizza)
                            if choice == "3":
                                pizza = SeafoodPizza()
                                order.add_pizza(pizza)
                except ValueError:
                    print("Некорректный ввод. Пожалуйста, введите целое число.")
                except OutOfStockError as e:
                    print(e)
                    print("На кухне нет такого количества пицц данного вида")
                except IncorrectInputError:
                    print(
                        "Некорректный ввод. Пожалуйста, выберите номер из меню или введите 'закончить'."
                    )
            else:
                print(
                    "Некорректный ввод. Пожалуйста, выберите номер из меню или введите 'закончить'."
                )
            self.order = order
        return order

    def display_menu(self):
        print("Меню:")
        print("1. Пепперони пицца")
        print("2. Барбекю пицца")
        print("3. Дары моря пицца")

    async def confirm_order_async(self):  # Изменим метод на асинхронный
        try:
            if not self.order:
                raise EmptyOrderError()
            print("Ваш заказ:")
            # Получаем список пицц в заказе
            pizzas = self.order.get_pizzas()
            for pizza in pizzas:
                print(f"{pizza.__class__.__name__}")
            print("Стоимость заказа: " + str(self.order.calculate_total()) + " рублей")
            confirm = input("Подтвердите заказ (да/нет): ")
            if confirm.lower() == "да":
                print("Заказ подтвержден.")
            else:
                print("Заказ отменен.")
        except EmptyOrderError as e:
            print(e)


async def main():
    # Создаем экземпляр терминала
    terminal = Terminal()

    # Показываем меню и берем заказ
    terminal.take_order()

    # Подтверждаем заказ асинхронно
    await terminal.confirm_order_async()


# Запускаем основную функцию
asyncio.run(main())
