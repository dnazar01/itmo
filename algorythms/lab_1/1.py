def binary_search(arr, x):
    steps = 0
    low = 0
    high = len(arr) - 1

    while (
        low <= high
    ):  # если использовать low<high, то мы не включим последний элемент в диапазоне поиска
        steps += 1
        mid = (low + high) // 2
        if arr[mid] == x:
            return steps
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1

    return steps


# Пример использования
arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
x = 19
steps = binary_search(arr, x)
print("Количество шагов для нахождения числа", x, "равно", steps)
