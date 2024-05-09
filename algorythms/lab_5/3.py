import bisect


def longest_increasing_subsequence(nums):
    if not nums:
        return 0, []

    n = len(nums)
    # Массив для хранения длин LIS длины i
    lis_lengths = [0] * n
    # Последние элементы LIS длины i
    last_elements = [0] * n

    # Начальные значения
    lis_lengths[0] = 1
    last_elements[0] = nums[0]
    max_length = 1

    for i in range(1, n):
        # Используем бинарный поиск для поиска наибольшего j, такого что nums[i] > last_elements[j]
        index = bisect.bisect_left(last_elements, nums[i], 0, max_length)
        if index == max_length:
            max_length += 1

        # Обновляем значения
        lis_lengths[i] = index + 1
        last_elements[index] = nums[i]

    # Восстановление LIS
    lis_sequence = []
    current_length = max_length
    for i in range(n - 1, -1, -1):
        if lis_lengths[i] == current_length:
            lis_sequence.append(nums[i])
            current_length -= 1

    lis_sequence.reverse()

    return max_length, lis_sequence


# Пример использования
nums = [10, 9, 2, 5, 3, 7, 101, 18]  # Пример массива чисел
length, sequence = longest_increasing_subsequence(nums)
print("Длина наибольшей непрерывной возрастающей подпоследовательности:", length)
print("Наибольшая непрерывная возрастающая подпоследовательность:", sequence)
