from abc import ABC, abstractmethod


class Deposit(ABC):
    def __init__(self, amount, duration, rate=0.05):
        self.__amount = amount
        self.__duration = duration
        self.__rate = rate

    def __lt__(self, other):
        if isinstance(other, Deposit):
            return self.profit() < other.profit()
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Deposit):
            return self.profit() <= other.profit()
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Deposit):
            return self.profit() > other.profit()
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Deposit):
            return self.profit() >= other.profit()
        return NotImplemented

    @abstractmethod
    def profit(self):
        pass

    # Геттеры и сеттеры для доступа к приватным атрибутам
    @property
    def amount(self):
        return self.__amount

    def set_amount(self, amount):
        self.__amount = amount

    @property
    def duration(self):
        return self.__duration

    def set_duration(self, duration):
        self.__duration = duration

    @property
    def rate(self):
        return self.__rate

    def set_rate(self, rate):
        self.__rate = rate


class TermDeposit(Deposit):
    def profit(self):
        # расчет прибыли для срочного вклада (простые проценты)
        profit = self.amount * self.rate * self.duration
        return profit


class BonusDeposit(Deposit):
    def __init__(self, amount, duration, bonus_threshold, bonus_rate, rate=0.05):
        super().__init__(amount, duration, rate)
        self.__bonus_threshold = bonus_threshold
        self.__bonus_rate = bonus_rate

    def profit(self):
        # расчет прибыли для бонусного вклада
        profit = self.amount * self.rate * self.duration
        if self.amount >= self.__bonus_threshold:
            bonus = profit * self.__bonus_rate
            profit += bonus
        return profit

    # Геттеры и сеттеры для доступа к приватным атрибутам
    def get_bonus_threshold(self):
        return self.__bonus_threshold

    def set_bonus_threshold(self, bonus_threshold):
        self.__bonus_threshold = bonus_threshold

    def get_bonus_rate(self):
        return self.__bonus_rate

    def set_bonus_rate(self, bonus_rate):
        self.__bonus_rate = bonus_rate


class CapitalizedDeposit(Deposit):
    def profit(self):
        # расчет прибыли для вклада с капитализацией процентов
        profit = self.amount * (1 + self.rate) ** self.duration - self.amount
        return profit


class Client(ABC):
    def __init__(self, name, deposit):
        self.__name = name
        self.__deposit = deposit

    @property
    def deposit(self):
        return self.__deposit

    def set_deposit(self, deposit):
        self.__deposit = deposit

    def get_profit(self):
        return self.__deposit.profit()

    # Геттер и сеттер для доступа к приватному атрибуту
    @property
    def name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name


def create_client():
    name = input("Привет! Как вас зовут? ")
    deposit = float(
        input(f"Рада вас видеть, {name}! Сколько вы готовы вложить в депозит? ")
    )
    print("Отлично! Теперь выберите тип вклада:")
    print("text_file.txt. Срочный вклад")
    print("2. Бонусный вклад")
    print("3. Вклад с капитализацией процентов")
    choice = input("Введите номер выбранного варианта: ")

    if choice == "text_file.txt":
        duration = int(input("На какой срок хотите сделать вклад (в месяцах)? "))
        Client(name, TermDeposit(deposit, duration))
    elif choice == "2":
        duration = int(input("На какой срок хотите сделать вклад (в месяцах)? "))
        return Client(name, BonusDeposit(deposit, duration, 1500, 0.01, 0.055))
    elif choice == "3":
        duration = int(input("На какой срок хотите сделать вклад (в месяцах)? "))
        return Client(name, CapitalizedDeposit(deposit, duration, 0.06))
    else:
        print("Некорректный выбор.")
        return None


if __name__ == "__main__":
    client = create_client()
    print(f"Спасибо, {client.name}! Ваш выбор учтен.")
    print(f"Прибыль по выбранному вкладу: {client.get_profit():,.2f} ₽ рублей.")
