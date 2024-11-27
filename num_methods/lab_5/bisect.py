import numpy as np

def f(x):
    return 3 * np.cos(2.5 * x) * np.exp((x**2) / 4 - 5)

def bisection(a, b, tol=1e-6):
    if f(a) * f(b) > 0:
        print("Функция не меняет знак на интервале")
        return None
    while (b - a) / 2 > tol:
        c = (a + b) / 2
        if f(c) == 0:
            break
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2

a, b = -0.7, -0.6
root_bisection = bisection(a, b)
print("Корень методом бисекции:", root_bisection)