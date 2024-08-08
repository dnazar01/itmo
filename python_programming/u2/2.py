class Country:
    def __init__(self, capital, population):
        try:
            self.__capital = capital
            if population <= 0:
                raise Exception
            self.__population = population
        except Exception:
            print("Население не может быть отрицательной величиной")

    def setPopulation(self, population):
        try:
            if population <= 0:
                raise Exception
            self.__population = population
        except Exception:
            print("Население не может быть отрицательной величиной")

    @property
    def captial(self):
        return self.__capital

    def getPopulation(self):
        return self.__population


class Russia(Country):
    def __init__(self):
        super().__init__("Moscow", 146447424)


class Germany(Country):
    def __init__(self):
        super().__init__("Berlin", 86607016)


class Canada(Country):
    def __init__(self):
        super().__init__("Ottawa", 40 * 10**6)


country1 = Russia()
country2 = Germany()
country3 = Canada()
print(country3.getPopulation())
print(country3.captial)
