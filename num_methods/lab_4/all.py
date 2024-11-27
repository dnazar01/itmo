import numpy as np
import matplotlib.pyplot as plt

# Исходные данные
A0 = np.array([
    [3, 1.5, 1, 0.75, 0.6, 0.5],
    [1.5, 1, 0.75, 0.6, 0.5, 0.4286],
    [1, 0.75, 0.6, 0.5, 0.4286, 0.375],
    [0.75, 0.6, 0.5, 0.4286, 0.375, 0.3333],
    [0.6, 0.5, 0.4286, 0.375, 0.3333, 0.3],
    [0.5, 0.4286, 0.375, 0.3333, 0.3, 0.2727]
])

b = np.array([-0.6677, -1.3026, -1.8363,
              -2.2722, -2.6154, -2.8710])

# Построение матрицы A
m = A0.shape[0]
E = np.eye(m)
A = A0 + m * E

def power_method(A, epsilon=1e-6, max_iterations=1000):
    n = A.shape[0]
    # Начальное приближение для собственного вектора
    x = np.random.rand(n)
    x = x / np.linalg.norm(x)
    lambda_old = 0

    for iteration in range(max_iterations):
        # Итерационный процесс
        x_new = A @ x
        x_new = x_new / np.linalg.norm(x_new)
        # Приближение собственного значения
        lambda_new = x_new @ (A @ x_new)

        # Проверка критерия сходимости
        if np.abs(lambda_new - lambda_old) < epsilon:
            break

        x = x_new
        lambda_old = lambda_new

    return lambda_new, x_new, iteration+1

# Применение степенного метода
lambda_max, eigenvector, iterations = power_method(A)
print(f"Максимальное собственное значение: {lambda_max}")
print(f"Собственный вектор:\n{eigenvector}")
print(f"Число итераций: {iterations}")

# Визуализация сходимости степенного метода
def power_method_convergence(A, epsilon=1e-6, max_iterations=1000):
    n = A.shape[0]
    x = np.random.rand(n)
    x = x / np.linalg.norm(x)
    lambda_old = 0
    lambdas = []

    for iteration in range(max_iterations):
        x_new = A @ x
        x_new = x_new / np.linalg.norm(x_new)
        lambda_new = x_new @ (A @ x_new)
        lambdas.append(lambda_new)

        if np.abs(lambda_new - lambda_old) < epsilon:
            break

        x = x_new
        lambda_old = lambda_new

    return lambda_new, x_new, iteration+1, lambdas

lambda_max, eigenvector, iterations, lambdas = power_method_convergence(A)

# Построение графика сходимости степенного метода
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(lambdas)+1), lambdas, marker='o')
plt.xlabel('Номер итерации')
plt.ylabel('Приближение собственного значения')
plt.title('Сходимость степенного метода')
plt.grid(True)
plt.savefig('power_method_convergence.png')
plt.show()

def iterative_method_convergence(A, b, tau, epsilon=1e-3, max_iterations=1000):
    x = np.zeros_like(b)
    errors = []

    for iteration in range(max_iterations):
        x_new = x - tau * (A @ x - b)
        error = np.linalg.norm(x_new - x)
        errors.append(error)
        x = x_new
        if error < epsilon:
            break

    return x_new, iteration+1, errors

tau = 1 / lambda_max
x_iterative, iter_count, errors = iterative_method_convergence(A, b, tau)
print(f"Решение методом простой итерации за {iter_count} итераций:")
print(x_iterative)

# Построение графика сходимости метода простой итерации
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(errors)+1), errors, marker='o')
plt.xlabel('Номер итерации')
plt.ylabel('Ошибка')
plt.title('Сходимость метода простой итерации')
plt.yscale('log')
plt.grid(True)
plt.savefig('iterative_method_convergence.png')
plt.show()

def jacobi_method_convergence(A, b, epsilon=1e-3, max_iterations=1000):
    x = np.zeros_like(b)
    errors = []
    D = np.diag(A)
    R = A - np.diagflat(D)

    for iteration in range(max_iterations):
        x_new = (b - R @ x) / D
        error = np.linalg.norm(x_new - x)
        errors.append(error)
        x = x_new
        if error < epsilon:
            break

    return x_new, iteration+1, errors

x_jacobi, jacobi_iterations, jacobi_errors = jacobi_method_convergence(A, b)
print(f"Решение методом Якоби за {jacobi_iterations} итераций:")
print(x_jacobi)

# Построение графика сходимости метода Якоби
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(jacobi_errors)+1), jacobi_errors, marker='o')
plt.xlabel('Номер итерации')
plt.ylabel('Ошибка')
plt.title('Сходимость метода Якоби')
plt.yscale('log')
plt.grid(True)
plt.savefig('jacobi_method_convergence.png')
plt.show()

# Решение системы с помощью встроенного метода для проверки
x_exact = np.linalg.solve(A, b)

# Вычисление нормы разности
diff_iterative = np.linalg.norm(x_exact - x_iterative)
diff_jacobi = np.linalg.norm(x_exact - x_jacobi)

print(f"Норма разности между точным решением и методом простой итерации: {diff_iterative}")
print(f"Норма разности между точным решением и методом Якоби: {diff_jacobi}")
