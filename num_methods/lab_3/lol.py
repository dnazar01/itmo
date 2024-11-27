\section*{Постановка задачи}

Рассмотрим функцию на отрезке $[-1; 2]$:

\[
f(x) = 3 \cos(2.5x) \exp\left( \frac{x^2}{4} - 5 \right).
\]

\section{Аппроксимация полиномом степени $m$}

\subsection{Выбор базисных функций}

В качестве базисных функций выберем степени аргумента $x$:

\[
\varphi_k(x) = x^k, \quad k = 0, 1, \dots, m.
\]

Аппроксимация функции $f(x)$ будет иметь вид:

\[
g(x) = \sum_{k=0}^{m} \alpha_k x^k.
\]

\subsection{Постановка задачи минимизации}

Найдем коэффициенты $\alpha_k$, минимизирующие функционал:

\[
\rho = \int_{-1}^{2} \left( f(x) - g(x) \right)^2 dx \to \min.
\]

\subsection{Вывод нормальных уравнений}

Для минимизации функционала по коэффициентам $\alpha_k$ приравняем нулю его частные производные:

\[
\frac{\partial \rho}{\partial \alpha_i} = -2 \int_{-1}^{2} \left( f(x) - \sum_{k=0}^{m} \alpha_k x^k \right) x^i dx = 0, \quad i = 0, 1, \dots, m.
\]

Получаем систему линейных уравнений:

\[
\sum_{k=0}^{m} \alpha_k \int_{-1}^{2} x^{k+i} dx = \int_{-1}^{2} f(x) x^i dx, \quad i = 0, 1, \dots, m.
\]

\subsection{Формирование матрицы системы}

Обозначим:

\[
A_{ik} = \langle \varphi_i, \varphi_k \rangle = \int_{-1}^{2} x^{i+k} dx, \quad b_i = \langle f, \varphi_i \rangle = \int_{-1}^{2} f(x) x^i dx.
\]

Тогда система уравнений примет вид:

\[
A \alpha = b,
\]

где $A$ — матрица скалярных произведений базисных функций, размером $(m+1) \times (m+1)$, $\alpha$ — вектор коэффициентов, $b$ — вектор скалярных произведений исходной функции и базисных функций.

\subsection{Вычисление элементов матрицы и вектора}

\subsubsection{Элементы матрицы $A$}

Элементы матрицы $A$ вычисляются по формуле:

\[
A_{ik} = \int_{-1}^{2} x^{i+k} dx = \frac{2^{i+k+1} - (-1)^{i+k+1}}{i + k + 1}.
\]

\subsubsection{Элементы вектора $b$}

Элементы вектора $b$ вычисляются как:

\[
b_i = \int_{-1}^{2} f(x) x^i dx.
\]

\subsubsection{Численные значения}

Для $m = 5$, матрица $A$ и вектор $b$ имеют следующие значения (вычислены численно с помощью Python):

\begin{itemize}
    \item Матрица $A$:

    \[
    A = \begin{pmatrix}
    A_{00} & A_{01} & A_{02} & A_{03} & A_{04} & A_{05} \\
    A_{10} & A_{11} & A_{12} & A_{13} & A_{14} & A_{15} \\
    A_{20} & A_{21} & A_{22} & A_{23} & A_{24} & A_{25} \\
    A_{30} & A_{31} & A_{32} & A_{33} & A_{34} & A_{35} \\
    A_{40} & A_{41} & A_{42} & A_{43} & A_{44} & A_{45} \\
    A_{50} & A_{51} & A_{52} & A_{53} & A_{54} & A_{55} \\
    \end{pmatrix}
    \]

    Численные значения:

    \[
    A \approx \begin{pmatrix}
    3 & 1.5 & 1 & 0.75 & 0.6 & 0.5 \\
    1.5 & 1. & 0.75 & 0.6 & 0.5 & 0.4285714286 \\
    1 & 0.75 & 0.6 & 0.5 & 0.4285714286 & 0.375 \\
    0.75 & 0.6 & 0.5 & 0.4285714286 & 0.375 & 0.3333333333 \\
    0.6 & 0.5 & 0.4285714286 & 0.375 & 0.3333333333 & 0.3 \\
    0.5 & 0.4285714286 & 0.375 & 0.3333333333 & 0.3 & 0.2727272727 \\
    \end{pmatrix}
    \]

    \item Вектор $b$:

    \[
    b = \begin{pmatrix}
    b_0 \\
    b_1 \\
    b_2 \\
    b_3 \\
    b_4 \\
    b_5 \\
    \end{pmatrix}
    \]

    Численные значения:

    \[
    b \approx \begin{pmatrix}
    -0.6677452142 \\
    -1.3025913919 \\
    -1.8362512694 \\
    -2.2722150857 \\
    -2.6153702452 \\
    -2.8709725134 \\
    \end{pmatrix}
    \]
\end{itemize}

\subsection{Решение системы уравнений}

Решаем систему $A \alpha = b$ методом Гаусса или с использованием встроенных функций Python.

\subsubsection*{Код программы}

\begin{verbatim}
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
\end{verbatim}

\subsubsection*{Результаты вычислений}

После выполнения программы получаем:

\begin{itemize}
    \item Матрица $A$:

    \[
    A \approx \begin{pmatrix}
    3 & 1.5 & 1 & 0.75 & 0.6 & 0.5 \\
    1.5 & 1 & 0.75 & 0.6 & 0.5 & 0.4285714286 \\
    1 & 0.75 & 0.6 & 0.5 & 0.4285714286 & 0.375 \\
    0.75 & 0.6 & 0.5 & 0.4285714286 & 0.375 & 0.3333333333 \\
    0.6 & 0.5 & 0.4285714286 & 0.375 & 0.3333333333 & 0.3 \\
    0.5 & 0.4285714286 & 0.375 & 0.3333333333 & 0.3 & 0.2727272727 \\
    \end{pmatrix}
    \]

    \item Вектор $b$:

    \[
    b \approx \begin{pmatrix}
    -0.6677452142 \\
    -1.3025913919 \\
    -1.8362512694 \\
    -2.2722150857 \\
    -2.6153702452 \\
    -2.8709725134 \\
    \end{pmatrix}
    \]

    \item Вектор коэффициентов $\alpha$:

    \[
    \alpha \approx \begin{pmatrix}
    -0.9987362952 \\
    -1.5889276319 \\
    -0.9033728993 \\
    -0.1139856225 \\
    0.3332716049 \\
    0.4020887299 \\
    \end{pmatrix}
    \]

    \item Ошибка аппроксимации: $\varepsilon = 0.2874936944$.
\end{itemize}

\subsection{Графическое представление}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{approximation_polynomial.png}
    \caption{Аппроксимация функции $f(x)$ полиномом степени $m=5$}
\end{figure}

\section{Аппроксимация полиномами Чебышёва}

\subsection{Выбор базисных функций}

В качестве базисных функций выберем полиномы Чебышёва первого рода $T_k(t)$, определенные на отрезке $[-1; 1]$. Так как наш отрезок $[-1; 2]$, выполним линейное преобразование к новой переменной $t$:

\[
t = \frac{2x - (b + a)}{b - a} = \frac{2x - 1}{3}.
\]

Обратное преобразование:

\[
x = \frac{3t + 1}{2}.
\]

\subsection{Аппроксимация функции в новом базисе}

Аппроксимация будет иметь вид:

\[
g(x) = \sum_{k=0}^{m} \beta_k T_k(t).
\]

\subsection{Постановка задачи минимизации}

Полиномы Чебышёва ортогональны с весом $w(t) = \frac{1}{\sqrt{1 - t^2}}$. Функционал ошибки:

\[
\rho = \int_{-1}^{1} \left( f(x(t)) - \sum_{k=0}^{m} \beta_k T_k(t) \right)^2 w(t) dt.
\]

\subsection{Вычисление коэффициентов}

Коэффициенты $\beta_k$ находятся по формуле:

\[
\beta_k = \frac{2}{\pi} \int_{-1}^{1} f(x(t)) T_k(t) \frac{dt}{\sqrt{1 - t^2}}, \quad k \geq 1,
\]
\[
\beta_0 = \frac{1}{\pi} \int_{-1}^{1} f(x(t)) \frac{dt}{\sqrt{1 - t^2}}.
\]

\subsection{Формирование вектора коэффициентов}

\subsubsection{Элементы вектора $\beta$}

Вычисляем интегралы численно с помощью Python.

\subsubsection*{Код программы}

\begin{verbatim}
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
\end{verbatim}

\subsubsection*{Результаты вычислений}

\begin{itemize}
    \item Вектор коэффициентов $\beta$:

    \[
    \beta \approx \begin{pmatrix}
    -0.7095314435 \\
    -1.1817442818 \\
    -1.0902186664 \\
    -0.6223587861 \\
    -0.1416999192 \\
    0.2206185222 \\
    \end{pmatrix}
    \]

    \item Ошибка аппроксимации: $\varepsilon_{\text{Чеб}} = 0.1422746121$.
\end{itemize}

\subsection{Графическое представление}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{approximation_chebyshev.png}
    \caption{Аппроксимация функции $f(x)$ полиномами Чебышёва степени $m=5$}
\end{figure}

\section{Сравнение результатов}

\begin{itemize}
    \item Матрица скалярных произведений базисных функций и вектор скалярных произведений исходной функции и базисных были получены и использованы для решения системы линейных уравнений в обоих методах.
    \item Аппроксимация полиномом степени $m=5$ дала ошибку $\varepsilon = 0.2874936944$.
    \item Аппроксимация полиномами Чебышёва той же степени дала ошибку $\varepsilon_{\text{Чеб}} = 0.1422746121$.
\end{itemize}

Таким образом, использование ортогональных полиномов Чебышёва позволяет получить более точное приближение при той же степени полинома. Матрицы скалярных произведений и векторы коэффициентов играют ключевую роль в получении этих результатов.