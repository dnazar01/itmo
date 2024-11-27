import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

# Задаем функцию f(x)
def f(x):
    return 3 * np.cos(2.5 * x) * np.exp(x**2 / 4 - 5)

# Пределы интегрирования
a, b = -1, 2

# Максимальная степень полинома
m = 5  # Как было определено ранее

# Формируем матрицу A и вектор b
A = np.zeros((m+1, m+1))
b_vec = np.zeros(m+1)

for i in range(m+1):
    for k in range(m+1):
        A[i, k], _ = quad(lambda x: x**(i + k), a, b)
    b_vec[i], _ = quad(lambda x: f(x) * x**i, a, b)

# Выводим матрицу A и вектор b
print("Матрица A:")
print(np.round(A, 10))
print("\nВектор b:")
print(np.round(b_vec, 10))

# Решаем систему уравнений
alpha = np.linalg.solve(A, b_vec)

# Выводим коэффициенты alpha
print("\nВектор коэффициентов alpha:")
print(np.round(alpha, 10))

# Создаем массив x для построения графиков
x_vals = np.linspace(a, b, 400)
f_vals = f(x_vals)
g_vals = np.polyval(alpha[::-1], x_vals)

# Вычисляем ошибку аппроксимации
error_func = lambda x: (f(x) - np.polyval(alpha[::-1], x))**2
error, _ = quad(error_func, a, b)

print(f"\nОшибка аппроксимации: {error:.10f}")

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(x_vals, f_vals, label='$f(x)$', linewidth=2)
plt.plot(x_vals, g_vals, label='$g(x)$', linestyle='--')
plt.title('Аппроксимация функции $f(x)$ полиномом степени $m$')
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.legend()
plt.grid(True)
plt.savefig('approximation_polynomial.png')
plt.show()