def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr):
    try:
        max_num = max(arr)
        exp = 1
        while max_num // exp > 0:
            counting_sort(arr, exp)
            exp *= 10
    except ValueError:
        print("Empty array")


def test_radix_sort():
    test_cases = [
        [],
        [5],
        [3, 5, 1, 8, 2],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [170, 45, 75, 90, 802, 24, 2, 66]
    ]

    for i, arr in enumerate(test_cases):
        sorted_arr = arr.copy()
        radix_sort(sorted_arr)
        assert sorted_arr == sorted(arr), f"Test case {i + 1} failed."

    print("All test cases passed.")


if __name__ == "__main__":
    test_radix_sort()
