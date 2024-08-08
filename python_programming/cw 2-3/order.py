from db import session, OrderModel


class Logger:  # класс миксин
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")


class Order:
    def __init__(self):
        self.pizzas = []

    def save(self):
        order = OrderModel(pizzas=self.pizzas)
        session.add(order)
        session.commit()
        self.pizzas = []

    def clear(self):
        for pizza in self.pizzas:
            session.delete(pizza)
        session.commit()
        self.pizzas = []

    def add_pizza(self, pizza_type, quantity):
        for _ in range(quantity):
            pizza = pizza_type()
            self.pizzas.append(pizza.db_entity)

    def calculate_total(self):
        total_cost = 0
        for pizza in self.pizzas:
            total_cost += pizza.cost
        return total_cost

    # Метод для получения списка пицц в заказе
    def get_pizzas(self):
        return self.pizzas
