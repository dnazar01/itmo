import numpy as np
import matplotlib.pyplot as plt
from scipy.special import eval_chebyt
from numpy.polynomial.chebyshev import chebgauss

# Задаем функцию f(x)
def f(x):
    return 3 * np.cos(2.5 * x) * np.exp(x**2 / 4 - 5)

# Пределы интегрирования
a, b = -1, 2

# Максимальная степень полинома
m = 5  # Как и в предыдущем случае

# Преобразование переменной
def x_to_t(x):
    return (2 * x - (b + a)) / (b - a)

def t_to_x(t):
    return ((b - a) * t + (b + a)) / 2

# Вычисляем коэффициенты beta_k с использованием квадратуры Гаусса-Чебышёва
beta = []

# Получаем узлы и веса квадратуры
n_points = 1000  # количество точек для квадратуры
t_nodes, weights = chebgauss(n_points)

for k in range(m+1):
    # Подынтегральная функция без учета веса
    f_values = f(t_to_x(t_nodes)) * eval_chebyt(k, t_nodes)
    # Интегрируем с учетом весов квадратуры
    integral = np.sum(f_values * weights)
    # Вычисляем коэффициенты beta_k
    if k == 0:
        beta_k = integral / np.pi
    else:
        beta_k = (2 * integral) / np.pi
    beta.append(beta_k)

# Выводим вектор beta
print("\nВектор коэффициентов beta:")
print(np.round(beta, 10))

# Создаем массив x для построения графиков
x_vals = np.linspace(a, b, 400)
t_vals = x_to_t(x_vals)
f_vals = f(x_vals)

# Вычисляем значения аппроксимации
g_cheb_vals = np.zeros_like(x_vals)
for k in range(m+1):
    g_cheb_vals += beta[k] * eval_chebyt(k, t_vals)

# Вычисляем ошибку аппроксимации
error_cheb_func = (f(t_to_x(t_nodes)) - sum(beta[k] * eval_chebyt(k, t_nodes) for k in range(m+1)))**2
error_cheb = np.sum(error_cheb_func * weights)

print(f"\nОшибка аппроксимации полиномами Чебышёва: {error_cheb:.10f}")

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(x_vals, f_vals, label='$f(x)$', linewidth=2)
plt.plot(x_vals, g_cheb_vals, label='$g_{Чеб}(x)$', linestyle='--')
plt.title('Аппроксимация функции $f(x)$ полиномами Чебышёва степени $m$')
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.legend()
plt.grid(True)
plt.savefig('approximation_chebyshev.png')  # Сохранение графика в файл
plt.show()