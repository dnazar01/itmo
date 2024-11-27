import numpy as np
import matplotlib.pyplot as plt

# Определяем функцию f(x) для задания
def f(x):
    return 3 * np.cos(2.5 * x) * np.exp(x**2 / 4 - 5)

# Функция для правой разностной производной
def forward_difference(func, x, h):
    return (func(x + h) - func(x)) / h

# Функция для центральной разностной производной
def central_difference(func, x, h):
    return (func(x + h) - func(x - h)) / (2 * h)

# Функция для второй разностной производной (используется для оценки ошибки правой производной)
def second_difference_approx(func, x, h):
    return (func(x + h) - 2 * func(x) + func(x - h)) / h**2

# Функция для третьей разностной производной (используется для оценки ошибки центральной производной)
def third_difference_approx(func, x, h):
    return (func(x + 2*h) - 3 * func(x + h) + 3 * func(x) - func(x - h)) / h**3

# Параметры
a, b = -1, 2  # границы интервала
h_forward = (b - a) / 20  # начальный шаг для правой производной
h_central = (b - a) / 20  # начальный шаг для центральной производной

# Точки для вычисления производных
x_values = np.linspace(a, b, 100)  # массив точек на интервале [-1, 2]
f_values = f(x_values)  # значения функции в этих точках

# Вычисление правой разностной производной
# Для правой производной точка x должна быть на 1 меньше, чем длина массива x_values, так как мы используем x + h
forward_derivatives = [forward_difference(f, x, h_forward) for x in x_values[:-1]]

# Вычисление центральной разностной производной
# Для центральной производной x должен быть на 1 меньше с каждой стороны
central_derivatives = [central_difference(f, x, h_central) for x in x_values[1:-1]]

# Оценка ошибки для правой разностной производной с использованием второй разностной производной
second_diffs = [second_difference_approx(f, x, h_forward) for x in x_values[1:-1]]
error_forward = np.max(np.abs(second_diffs)) * h_forward / 2

# Оценка ошибки для центральной разностной производной с использованием третьей разностной производной
third_diffs = [third_difference_approx(f, x, h_central) for x in x_values[2:-2]]
error_central = np.max(np.abs(third_diffs)) * h_central**2 / 6

# Построение графиков правой и центральной разностных производных
plt.figure(figsize=(10, 6))
plt.plot(x_values[:-1], forward_derivatives, label="Правая разностная производная")
plt.plot(x_values[1:-1], central_derivatives, label="Центральная разностная производная", linestyle='--')
plt.title("Численные производные функции f(x) на отрезке [-1, 2]")
plt.xlabel("x")
plt.ylabel("Производная")
plt.legend()
plt.grid(True)
plt.show()

# Вывод значений ошибок
print("Оценка ошибки для правой разностной производной:", error_forward)
print("Оценка ошибки для центральной разностной производной:", error_central)
