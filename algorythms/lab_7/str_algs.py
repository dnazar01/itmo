# общая часть


def prime(n):  # Простые числа
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


numbers = []
numb = 2
alphabet = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
while len(numbers) != 500:
    if prime(numb):
        numbers.append(str(numb))
    numb += 1
string_numbers = "".join(numbers)


# наивный поиск
def naive(numb_string):  # наивный поиск
    count_numb = [0 for i in range(0, 100)]
    for i in range(0, len(numb_string) - 1):
        count_numb[int(numb_string[i] + numb_string[i + 1])] += 1  # xn
    print(max(count_numb))


naive(string_numbers)


# алгоритм Рабина-Карпа
def alg(numb_string):
    HashlistLine = []
    unique_numb = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    len_alphabet = 10
    for i in range(len(numb_string) - 1):
        Hash = unique_numb.index(int(numb_string[i])) * len_alphabet ** (
            1
        ) + unique_numb.index(int(numb_string[i + 1])) * len_alphabet ** (0)
        HashlistLine.append(Hash)
    return HashlistLine


hashList = [l for l in range(0, 100)]
NewHashList = [0 for i in range(0, 10)]
for i in range(len(hashList)):
    if hashList[i] > 9:
        timeI = str(hashList[i])
        NewItemHasList = (
            alphabet.index(int(timeI[0])) * 10**1
            + alphabet.index(int(timeI[-1])) * 10**0
        )
        NewHashList.append(NewItemHasList)

count = [0 for i in range(100)]
funcList = alg(string_numbers)
for i in range(len(NewHashList)):
    for j in range(len(funcList)):
        if NewHashList[i] == funcList[j]:
            count[i] += 1

print(max(count))


# Алгоритм Бойера-Мура
def check(pattern, substring):
    for j in range(1, -1, -1):
        if pattern[j] != substring[j]:
            return False
    return True


def BoyerMoor(numb_string, pattern):
    cnt = 0
    i = 0
    while i < len(numb_string) - 1:
        substring = numb_string[i] + numb_string[i + 1]
        if check(pattern, substring):
            cnt += 1
            i += 2
        else:
            if pattern[0] == substring[-1]:
                i += 1
            else:
                i += 2
    return cnt


count2 = [0 for n in range(0, 100)]
for i in range(10, 100):
    count2[i] = BoyerMoor(string_numbers, str(i))
print(max(count2))


# Алгоритм Кнута Морриса Пратта
def KMP(numb_string):
    for i in range(10, 100):
        image = str(i)
        if numb_string[0] == numb_string[1]:
            image_arr = [0, 1]
        else:
            image_arr = [0, 0]
        j = 0
        while j < len(numb_string) - 1:
            for k in range(len(image)):
                if numb_string[j + k] != image[k]:
                    j += (image_arr[k - 1] + 1) if k == 1 else 1
                    break
            else:
                mass[int(image)] += 1
                j += 1


mass = [0 for i in range(0, 100)]
KMP(string_numbers)
print(max(mass))
