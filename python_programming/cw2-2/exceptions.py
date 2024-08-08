class PizzaError(Exception):
    """Базовый класс исключений для ошибок, связанных с пиццей."""

    pass


class IncorrectInputError(PizzaError):
    """Исключение, возникающее при некорректном вводе пользователя."""

    def __init__(
        self,
        message="Некорректный ввод. Пожалуйста, выберите номер из меню или введите 'закончить'.",
    ):
        self.message = message
        super().__init__(self.message)


class OutOfStockError(PizzaError):
    """Исключение, возникающее при попытке заказать больше, чем есть в наличии."""

    def __init__(self, item):
        self.item = item
        super().__init__(f"На кухне нет такого количества пицц '{item}' данного вида.")


class EmptyOrderError(PizzaError):
    """Исключение, возникающее при попытке подтверждения пустого заказа."""

    def __init__(self):
        super().__init__("Невозможно подтвердить пустой заказ.")
