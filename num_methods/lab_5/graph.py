import numpy as np
import matplotlib.pyplot as plt

# Определим функцию
def f(x):
    return 3 * np.cos(2.5 * x) * np.exp((x**2) / 4 - 5)

# Генерируем значения x для графика
x_vals = np.linspace(-1, 2, 400)
y_vals = f(x_vals)

# Строим график функции
plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_vals, label=r'$f(x) = 3 \cos(2.5x) \exp\left(\frac{x^2}{4} - 5\right)$')
plt.axhline(0, color='black',linewidth=1)  # Ось X
plt.axvline(0, color='black',linewidth=1)  # Ось Y
plt.grid(True)
plt.title(r'График функции $f(x)$ на интервале $[-1, 2]$')
plt.xlabel('$x$')
plt.ylabel('$f(x)$')
plt.legend()
plt.savefig('function_graph.png')
plt.show()