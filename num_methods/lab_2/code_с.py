import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Определяем функцию
def f(x):
    return 3 * np.cos(2.5 * x) * np.exp(x**2 / 4 - 5)

# Интервал интегрирования
a = -1
b = 2

# Реализация составной формулы трапеций
def composite_trapezoidal_rule(f, a, b, n):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)  # n+1 точек
    y = f(x)
    I = h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])
    return I

# Число узлов
n1 = 20
n2 = 40

# Вычисляем интегралы
I_20 = composite_trapezoidal_rule(f, a, b, n1)
I_40 = composite_trapezoidal_rule(f, a, b, n2)

print(f"Интеграл с {n1} узлами: {I_20}")
print(f"Интеграл с {n2} узлами: {I_40}")
print(f"Разница между оценками: {abs(I_40 - I_20)}")

# Оценка максимума второй производной с использованием конечных разностей
N = 1000
x_dense = np.linspace(a, b, N)
h_dense = x_dense[1] - x_dense[0]
f_values = f(x_dense)

# Приближение второй производной
fpp = np.zeros_like(x_dense)
for i in range(1, N - 1):
    fpp[i] = (f_values[i - 1] - 2 * f_values[i] + f_values[i + 1]) / h_dense**2

max_fpp = np.max(np.abs(fpp[1:-1]))  # Исключаем концевые точки, где приближение некорректно

# Оценка погрешности
h1 = (b - a) / n1
Error_estimate_20 = ((b - a) * h1**2 / 12) * max_fpp

h2 = (b - a) / n2
Error_estimate_40 = ((b - a) * h2**2 / 12) * max_fpp

print(f"Оценка погрешности для {n1} узлов: {Error_estimate_20}")
print(f"Оценка погрешности для {n2} узлов: {Error_estimate_40}")

# Уточнение значения интеграла с помощью экстраполяции Ричардсона
I_extrapolated = (4 * I_40 - I_20) / 3
print(f"Уточненная оценка интеграла с помощью экстраполяции Ричардсона: {I_extrapolated}")

# Вычисляем точное значение интеграла с помощью scipy.integrate.quad для сравнения
I_exact, _ = quad(f, a, b)
print(f"Точное значение интеграла (с использованием quad): {I_exact}")

# Вычисляем абсолютные погрешности
Error_20 = abs(I_20 - I_exact)
Error_40 = abs(I_40 - I_exact)
Error_extrapolated = abs(I_extrapolated - I_exact)

print(f"Абсолютная погрешность при {n1} узлах: {Error_20}")
print(f"Абсолютная погрешность при {n2} узлах: {Error_40}")
print(f"Абсолютная погрешность уточненной оценки: {Error_extrapolated}")

# Построение графика функции f(x)
plt.figure(figsize=(10, 6))
plt.plot(x_dense, f_values, label='f(x)')
plt.title('Функция f(x)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()
plt.show()

# Построение графика приближенной второй производной
plt.figure(figsize=(10, 6))
plt.plot(x_dense[1:-1], fpp[1:-1], label='Приближенная f\'\'(x)', color='orange')
plt.title('Приближенная вторая производная f\'\'(x)')
plt.xlabel('x')
plt.ylabel('f\'\'(x)')
plt.grid(True)
plt.legend()
plt.show()
