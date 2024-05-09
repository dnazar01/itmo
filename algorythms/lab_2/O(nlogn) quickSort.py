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


n = int(input())
a = list(map(int, input().split()))
a = quickSort(a)
for i in a:
    print(i, end=" ")
