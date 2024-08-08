class Math:
    @staticmethod
    def addition(a, b):
        return a + b

    @staticmethod
    def multiplication(a, b):
        return a * b

    @staticmethod
    def division(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return "Ошибка: деление на ноль"

    @staticmethod
    def substraction(a, b):
        return a - b


print(Math.addition(3, 4))
print(Math.division(5, 0))
