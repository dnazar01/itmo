import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from math import factorial

# Обозначаем переменные и символы
sin = sp.sin
x = sp.symbols('x')


# Определяем основную функцию
def my_function(x):
    return 3 * sp.cos(2.5 * x) * sp.exp(x ** 2 / 4 - 5)


# Интервалы и количество узлов
a = -1
b = 2
m = 4  # Число узлов (индексы от 0 до 4)

# Узлы интерполяции
x_nodes = [-1.0, -0.25, 0.5, 1.25, 2.0]
y_nodes = [my_function(x) for x in x_nodes]


# Функция для вычисления интерполяционного полинома Лагранжа
def compute_lagrange_polynomial(x, x_nodes, y_nodes, m):
    P = 0
    for k in range(m + 1):
        l_k = 1
        for i in range(m + 1):
            if i != k:
                l_k *= (x - x_nodes[i]) / (x_nodes[k] - x_nodes[i])
        P += l_k * y_nodes[k]
    return P


# Полином Лагранжа для заданных значений
Lagrange_poly = compute_lagrange_polynomial(x, x_nodes, y_nodes, m)
expanded_Lagrange_poly = sp.expand(Lagrange_poly)
expanded_Lagrange_poly_numeric = expanded_Lagrange_poly.evalf(10)


# Построение графика функции и интерполяционного полинома Лагранжа
def plot_lagrange_and_function(x, x_nodes, y_nodes, m):
    x_values = np.linspace(a, b, 1000)
    f_numeric = sp.lambdify(x, my_function(x), "numpy")
    L_numeric = sp.lambdify(x, expanded_Lagrange_poly, "numpy")

    plt.plot(x_values, f_numeric(x_values), label='Оригинальная функция', color='blue')
    plt.plot(x_values, L_numeric(x_values), label='Полином Лагранжа', color='red')
    plt.scatter(x_nodes, [float(yi) for yi in y_nodes], color='red', zorder=5, s=20, label='Узлы интерполяции')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Интерполяционный полином Лагранжа и функция')
    plt.legend()
    plt.show()


# Максимальная теоретическая ошибка интерполяции
def theoretical_max_error(x_values, max_derivative, m, x_nodes):
    error_terms = np.ones_like(x_values)
    for x_node in x_nodes:
        error_terms *= (x_values - x_node)
    max_error = (np.abs(max_derivative) / factorial(m + 1)) * np.abs(error_terms)
    return max_error


# Вычисляем производную нужного порядка (m+1 раз)
derivative = sp.diff(my_function(x), x, m + 1)

# Максимум производной на интервале
max_derivative_value = max([abs(derivative.subs(x, val)) for val in x_nodes])
print("Максимальное значение производной пересчитано: ", max_derivative_value)



# Расчет фактической ошибки интерполяции
def compute_actual_error(x_values):
    f_numeric = sp.lambdify(x, my_function(x), "numpy")
    L_numeric = sp.lambdify(x, expanded_Lagrange_poly, "numpy")
    return np.abs(f_numeric(x_values) - L_numeric(x_values))


# Построение графика фактической и максимальной погрешности
def plot_actual_and_max_error(a, b, m, max_derivative_value, x_nodes, y_nodes):
    x_values = np.linspace(a, b, 1000)

    # Вычисляем фактическую и теоретическую погрешность
    actual_error = compute_actual_error(x_values)
    max_error = theoretical_max_error(x_values, max_derivative_value, m, x_nodes)

    # График фактической погрешности
    plt.plot(x_values, actual_error, label='Фактическая ошибка', color='blue')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('Ошибка')
    plt.title('График фактической ошибки интерполяции')
    plt.legend()
    plt.show()

    # График фактической и максимальной погрешности
    plt.plot(x_values, actual_error, label='Фактическая ошибка', color='blue')
    plt.plot(x_values, max_error, label='Теоретическая ошибка', color='red')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('Ошибка')
    plt.title('Фактическая и теоретическая погрешность')
    plt.legend()
    plt.show()


# Вывод полинома и погрешностей
print("Интерполяционный полином Лагранжа: ", expanded_Lagrange_poly_numeric)
print("Максимальное значение производной: ", max_derivative_value)

# Построение графиков
plot_lagrange_and_function(x, x_nodes, y_nodes, m)
plot_actual_and_max_error(a, b, m, max_derivative_value, x_nodes, y_nodes)

# Вывод значений y в узлах
for i, (x_val, y_val) in enumerate(zip(x_nodes, y_nodes), start=0):
    print(f"Узел {i}: y = {y_val}")

