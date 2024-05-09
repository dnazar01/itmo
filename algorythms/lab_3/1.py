import timeit
import random


def quickSort(a):
    if len(a) <= 1:
        return a
    pivot = random.randint(0, len(a) - 1)
    mas1 = quickSort(a[:pivot])
    mas2 = quickSort(a[pivot:])
    return merge(mas1, mas2)


def merge(a, b):
    res = []
    len_a = len(a)
    len_b = len(b)
    a_pointer = 0
    b_pointer = 0
    while a_pointer < len_a and b_pointer < len_b:
        if a[a_pointer] < b[b_pointer]:
            res.append(a[a_pointer])
            a_pointer += 1
        else:
            res.append(b[b_pointer])
            b_pointer += 1
    while a_pointer < len_a:
        res.append(a[a_pointer])
        a_pointer += 1
    while b_pointer < len_b:
        res.append(b[b_pointer])
        b_pointer += 1
    return res


def comb_sort(arr):
    gap = len(arr)
    shrink = 1.3
    sorted = False
    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        i = 0
        sorted = True
        while i + gap < len(arr):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
            i += 1
    return arr


# Генерируем случайный массив для сортировки
arr = [random.randint(1, 1000000) for _ in range(100000)]

# Оценка времени выполнения для быстрой сортировки
quick_sort_time = timeit.timeit(lambda: quickSort(arr.copy()), number=1)

# Оценка времени выполнения для сортировки расческой
comb_sort_time = timeit.timeit(lambda: comb_sort(arr.copy()), number=1)

print("Время выполнения быстрой сортировки:", quick_sort_time)
print("Время выполнения сортировки расческой:", comb_sort_time)


# Суть сортировки расческой заключается в том, что мы начинаем с большого промежутка между сравниваемыми элементами
# и постепенно его уменьшаем, "расчесывая" массив. Это позволяет перемещать большие элементы в конец массива быстрее,
# что уменьшает количество перестановок. Коэффициент уменьшения промежутка text_file.txt.3 является оптимальным для этого метода.

# Алгоритм заканчивает свою работу, когда промежуток становится равным text_file.txt, что приводит к завершению
# сортировки методом расчески.
