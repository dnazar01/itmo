def matrix_chain_order(p):
    n = len(p) - 1
    m = [
        [0] * n for _ in range(n)
    ]  # Матрица для хранения минимального количества операций
    s = [
        [0] * n for _ in range(n)
    ]  # Матрица для хранения оптимальных точек разделения цепочки

    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            m[i][j] = float("inf")
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    return m, s


def print_optimal_parens(s, i, j):
    if i == j:
        print("A" + str(i + 1), end="")
    else:
        print("(", end="")
        print_optimal_parens(s, i, s[i][j])
        print_optimal_parens(s, s[i][j] + 1, j)
        print(")", end="")


# Пример использования
matrix_sizes = [10, 2000, 100, 40, 550, 3432]  # Размеры матриц в цепочке умножения
min_ops, optimal_splits = matrix_chain_order(matrix_sizes)
print("Минимальное количество скалярных операций:", min_ops[0][-1])
print("Оптимальный порядок умножения:", end=" ")
print_optimal_parens(optimal_splits, 0, len(matrix_sizes) - 2)
