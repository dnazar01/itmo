import numpy as np
import numdifftools as nd

# Определим функцию
def f(x):
    return 3 * np.cos(2.5 * x) * np.exp((x**2) / 4 - 5)

# Численное вычисление производной
def newton_method(x0, tol=1e-6, max_iter=100):
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        fpx = nd.Derivative(f)(x)  # Используем numdifftools для вычисления производной
        if fpx == 0:
            break
        x_next = x - fx / fpx
        if abs(x_next - x) < tol:
            return x_next
        x = x_next
    return x

root_newton = newton_method(-0.5)
print("Корень методом Ньютона:", root_newton)
