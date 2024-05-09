import timeit
import random

# Генерируем случайный массив из 100000 элементов
array = [random.randint(1, 1000) for _ in range(100000)]

# Функция для преобразования массива в кучу
def heapify(array, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and array[i] < array[l]:
        largest = l
    if r < n and array[largest] < array[r]:
        largest = r

    if largest != i:
        array[i], array[largest] = array[largest], array[i]
        heapify(array, n, largest)

# Функция для сортировки массива с использованием пирамидальной сортировки
def heapSort(array):
    n = len(array)
    # Строим кучу из массива
    for i in range(n // 2, -1, -1):
        heapify(array, n, i)
    # Извлекаем элементы по одному из кучи
    for i in range(n - 1, 0, -1):
        array[i], array[0] = array[0], array[i]
        heapify(array, i, 0)
    return array

# Функция для сортировки массива с использованием блочной сортировки
def bucketSort(array):
    largest = max(array)
    length = len(array)
    size = largest / length

    # Создаем пустые корзины
    buckets = [[] for i in range(length)]

    # Распределяем элементы по корзинам
    for i in range(length):
        index = int(array[i] / size)
        if index != length:
            buckets[index].append(array[i])
        else:
            buckets[length - 1].append(array[i])

    # Сортируем каждую корзину и объединяем их
    for i in range(len(array)):
        buckets[i] = sorted(buckets[i])

    result = []
    for i in range(length):
        result = result + buckets[i]

    return result

# Реализация сортировки слиянием
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        merge_sort(left_half)
        merge_sort(right_half)
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# Замеряем время выполнения каждого метода сортировки
bucket_sort_time = timeit.timeit(lambda: bucketSort(array.copy()), number=1)
heap_sort_time = timeit.timeit(lambda: heapSort(array.copy()), number=1)
merge_sort_time = timeit.timeit(lambda: merge_sort(array.copy()), number=1)

# Выводим результаты
print("Время выполнения блочной сортировки:", bucket_sort_time)
print("Время выполнения пирамидальной сортировки:", heap_sort_time)
print("Время выполнения сортировки слиянием:", merge_sort_time)
