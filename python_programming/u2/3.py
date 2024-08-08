class Dog:
    def __init__(self, name, age):
        try:
            self.__name = name
            if 0 <= age <= 20:
                self.__age = age
            else:
                raise Exception
        except Exception:
            print("Население не может быть отрицательной величиной")

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        try:
            if 0 <= age <= 20:
                self.__age = age
            else:
                raise Exception
        except Exception:
            print("Население не может быть отрицательной величиной")

    @name.setter
    def name(self, name):
        self.__name = name


class ToyTerier(Dog):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.__voice = "Голос терьера"

    def seatHome(self):
        print(f"Терьер {super().name} сидит дома")

    @property
    def voice(self):
        return self.__voice


class Spaniel(Dog):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.__voice = "Голос спаниэля"

    def hunt(self):
        print(f"Спаниэль {super().name} охотится")


class GermanOvcharka(Dog):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.__voice = "Голос немечкой овчарки"

    def stay(self):
        print(f"Овчарка {super().name} сторожить")


dog1 = ToyTerier("Bobik", 1)
dog2 = ToyTerier("Vaska", 2)

dog3 = Spaniel("Borya", 10)
dog4 = Spaniel("Lola", 4)

dog5 = GermanOvcharka("Solo", 7)
dog6 = GermanOvcharka("Poke", 9)

dog1.seatHome()
print(dog1.voice)
