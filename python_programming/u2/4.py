import math


class Figure:
    def __init__(self, color="White"):
        self.__color = color

    def setColor(self, color):
        self.__color = color

    @property
    def color(self):
        return self.__color


class Square(Figure):
    def __init__(self, side1, side2):
        super().__init__()
        try:
            if side1 < 0 or side2 < 0:
                raise Exception
            self.__side1 = side1
            self.__side2 = side2
        except Exception:
            print("Сторона квадрата не может быть отрицательным")

    def setColor(self, color):
        self.__color = color
        print("Изменен цвет для квадрата")

    def getInfo(self):
        print(
            f"Квадрат\nСторона 1: {self.__side1}\nСторона 2: {self.__side2}\nПлощадь: {self.__side1 * self.__side2}\nЦвет: {super().color}"
        )


class Circle(Figure):
    def __init__(self, radius):
        super().__init__()
        try:
            if radius < 0:
                raise Exception
            self.__radius = radius
        except Exception:
            print("Радиус квадрата не может быть отрицательным")

    def setColor(self, color):
        self.__color = color
        print("Изменен цвет для круга")

    def getInfo(self):
        print(
            f"Круг\nРадиус: {self.__radius}\nПлощадь: {self.__radius ** 2 * math.pi}\nЦвет: {super().color}"
        )


fig1 = Circle(5)
fig1.getInfo()
fig2 = Circle(-1)
