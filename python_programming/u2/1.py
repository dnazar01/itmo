class Student:
    def __init__(self, name="Radomir", groupNumber=1213, age=18):
        self.__name = name
        self.__groupNumber = groupNumber
        self.__age = age

    def show_info(self):
        print(
            f"Студент\nИмя:{self.__name}\nНомер группы:{self.__groupNumber}\nВозраст:{self.__age}"
        )

    @property
    def name(self):
        return self.__name

    @property
    def groupNumber(self):
        return self.__groupNumber

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        self.__age = age

    @groupNumber.setter
    def groupNumber(self, groupNumber):
        self.__groupNumber = groupNumber


s1 = Student("Vasya", 1209, 20)
s2 = Student()
s3 = Student("Jenya", 1609, 21)
s4 = Student("Vanya", 1899, 17)
s5 = Student("Sasha", 829, 23)
students = [s1, s2, s3, s4, s5]
for student in students:
    student.show_info()
    print("\n")
