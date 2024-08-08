class Progression:
    @staticmethod
    def calc_arifm():
        a = int(input("Введите а1 для прогрессии: "))
        d = int(input("Введите разность прогрессии: "))
        n = int(input("Введите номер нужного члена прогрессии: "))
        print(f"{n}-ый член арифм прогрессии равен: {a + d * (n - 1)}")

    @staticmethod
    def calc_geom():
        b = int(input("Введите b1 для прогрессии: "))
        q = int(input("Введите множитель прогрессии: "))
        n = int(input("Введите номер нужного члена прогрессии: "))
        print(f"{n}-ый член арифм прогрессии равен: {b + q ** (n - 1)}")


Progression.calc_geom()
