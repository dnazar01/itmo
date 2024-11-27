import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from math import pi, factorial

# Определение символьной переменной для полиномов
x = sp.symbols('x')

# Пределы интервала для интерполяции
a = -1
b = 2

# Символьное выражение функции
def original_function_symbolic(x):
    return 3 * sp.cos(2.5 * x) * sp.exp(x**2 / 4 - 5)

# Численная версия функции
def original_function_numeric(x):
    return 3 * np.cos(2.5 * x) * np.exp(x**2 / 4 - 5)

# Вычисление производных до 6-го порядка
f = original_function_symbolic(x)
derivatives = [sp.diff(f, x, i) for i in range(3, 7)]

# Преобразование производных в численные функции
derivative_functions = [sp.lambdify(x, derivative, "numpy") for derivative in derivatives]

# Определение максимальных значений производных на интервале для использования в теоретической ошибке
x_test = np.linspace(a, b, 1000)
M_max_values = {}

for i, derivative_func in enumerate(derivative_functions, start=3):
    max_value = np.max(np.abs(derivative_func(x_test)))
    M_max_values[i] = max_value
    print(f"Максимальное значение {i}-й производной на интервале [{a}, {b}]: {max_value}")

# Функция для вычисления полинома Лагранжа
def lagrange_polynomial(x, x_nodes, y_nodes, degree):
    P = 0
    for k in range(degree + 1):
        l_k = 1
        for i in range(degree + 1):
            if i != k:
                l_k *= (x - x_nodes[i]) / (x_nodes[k] - x_nodes[i])
        P += l_k * y_nodes[k]
    return P

for degree in range(3, 7):  # Цикл для полиномов от 3 до 6 степени
    # Функция для нахождения узлов Чебышева
    def chebyshev_nodes(a, b, degree):
        nodes = []
        values = []
        for i in range(1, degree + 2):
            x_cheb = ((a + b) / 2) + ((b - a) / 2) * np.cos((pi * (2 * i - 1)) / (2 * (degree + 1)))
            nodes.append(x_cheb)
            values.append(original_function_numeric(x_cheb))
        return nodes, values

    # Функция для построения графика полинома Лагранжа и исходной функции
    def plot_polynomial_and_function(a, b, x_nodes_cheb, y_values_cheb, degree):
        polynomial = lagrange_polynomial(x, x_nodes_cheb, y_values_cheb, degree)
        expanded_polynomial = sp.expand(polynomial)

        # Вывод полинома Лагранжа с преобразованием степени
        polynomial_str = str(expanded_polynomial).replace('**', '^')
        print(polynomial_str)

        # Создание численных значений для построения графиков
        x_values = np.linspace(a, b, 1000)
        polynomial_numeric = sp.lambdify(x, expanded_polynomial, "numpy")
        plt.plot(x_values, original_function_numeric(x_values), label='Исходная функция', color='blue')
        plt.plot(x_values, polynomial_numeric(x_values), label=f'Полином Лагранжа {degree} степени', color='red')
        plt.scatter(x_nodes_cheb, y_values_cheb, color='red', zorder=5, s=20, label='Узлы Чебышева')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend(loc='lower left', fontsize='xx-small')
        plt.title(f'Интерполяция с узлами Чебышева: полином {degree} степени')
        plt.show()

    # Функция для расчета теоретической максимальной ошибки
    def calculate_max_error(x_values, M_max, degree, x_nodes):
        weight_function = np.ones_like(x_values)
        for x_k in x_nodes:
            weight_function *= (x_values - x_k)
        return (np.abs(M_max) / factorial(degree + 1)) * np.abs(weight_function)

    # Функция для вычисления фактической ошибки
    def actual_error(x_values, x_nodes_cheb, y_values_cheb, degree):
        Lagrange_polynomial = lagrange_polynomial(x, x_nodes_cheb, y_values_cheb, degree)
        polynomial_numeric = sp.lambdify(x, Lagrange_polynomial, "numpy")
        return np.abs(original_function_numeric(x_values) - polynomial_numeric(x_values))

    # Функция для отображения фактической и максимальной погрешностей
    def plot_errors(a, b, degree, M_max, x_nodes_cheb, y_values_cheb):
        x_values = np.linspace(a, b, 1000)

        # Вычисление фактической и максимальной ошибок
        actual_err = actual_error(x_values, x_nodes_cheb, y_values_cheb, degree)
        max_err = calculate_max_error(x_values, M_max, degree, x_nodes_cheb)

        # График фактической ошибки
        plt.plot(x_values, actual_err, label='Фактическая погрешность', color='blue')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('Погрешность')
        plt.title(f'Фактическая погрешность интерполяции: полином {degree} степени')
        plt.legend(loc='lower left', fontsize='xx-small')
        plt.show()

        # График фактической и максимальной ошибок
        plt.plot(x_values, actual_err, label='Фактическая погрешность', color='blue')
        plt.plot(x_values, max_err, label='Теоретическая погрешность', color='red')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('Погрешность')
        plt.legend(loc='upper left', fontsize='xx-small')
        plt.title(f'Фактическая и максимальная погрешности интерполяции: \n полином {degree} степени')
        plt.show()

    # Получение узлов Чебышева и соответствующих значений функции
    x_nodes_cheb, y_values_cheb = chebyshev_nodes(a, b, degree)
    print(f"Узлы Чебышева и значения функции для полинома {degree} степени:")
    for i, (x_val, y_val) in enumerate(zip(x_nodes_cheb, y_values_cheb)):
        print(f"x_{i} = {x_val:.10f}, f(x_{i}) = {y_val:.10f}")

    # Построение графика полинома Лагранжа
    print(f"Интерполяционный полином Лагранжа для степени {degree}:")
    plot_polynomial_and_function(a, b, x_nodes_cheb, y_values_cheb, degree)

    # Значение M_max для текущей степени
    M_max = M_max_values[degree]
    print(f"Значение M_max для полинома {degree} степени: {M_max}")

    # Построение графиков ошибок
    plot_errors(a, b, degree, M_max, x_nodes_cheb, y_values_cheb)
