class Soda:
    def __init__(self, type=None):
        self.type = type

    def show_my_drink(self):
        if self.type is None:
            return f"Обычная газировка"
        return f"Газировка и {self.type}"


cola = Soda("крем")
print(cola.show_my_drink())
