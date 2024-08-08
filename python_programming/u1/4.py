class WrongYearException(Exception):
    pass


class Car:
    def __init__(self, color, type, year):
        try:
            self.__color = color
            self.__type = type
            if 1886 <= year <= 2024:
                self.__year = year
                self.__is_on = False
            else:
                raise WrongYearException
        except WrongYearException:
            print("Ошибка: год должен быть не больше текущего и не меньше 1886")

    def turn_on(self):
        if not self.__is_on:
            self.__is_on = True
            print("Автомобиль заведен")
        else:
            print("Ошибка: нельзя завести уже заведенный автомобиль!")

    def turn_off(self):
        if self.__is_on:
            self.__is_on = False
            print("Автомобиль заглушен")
        else:
            print("Ошибка: нельзя остановить уже остановленный автомобиль!")

    def set_year(self, year):
        self.__year = year

    def set_type(self, type):
        self.__type = type

    def set_color(self, color):
        self.__color = color

    def get_info(self):
        print(f"Автомобиль\nЦвет:{self.__color}\nТип:{self.__type}\nГод:{self.__year}")


car = Car("blue", "Jeep", 1886)
car.turn_on()
car.turn_on()
car.get_info()
car.turn_off()
car.turn_off()
