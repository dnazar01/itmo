import random

# Получение строки от пользователя
a = input("Введите строку ")

# Создание массива для хранения ASCII кодов символов строки
arr = []
for i in range(len(a)):
    arr.append(ord(a[i]))

# Создание массива для хранения хэша
hash = []

# Генерация случайной константы C
C = random.uniform(0, 1)

# Применение хэш-функции к каждому ASCII коду символа строки
for i in range(len(arr)):
    Key = arr[i]
    M = len(arr)

    # Вычисление значения хэша для текущего символа
    res = round(M * ((Key * C) % 1))
    hash.append(str(res))

# Преобразование массива хэша в строку
print("".join(hash))
