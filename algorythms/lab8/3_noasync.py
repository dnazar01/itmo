import time

t1 = time.time()


def process_file(file_name):
    f = open(file_name)
    cnt = 0
    for symb in f.read():
        if symb == "a":
            cnt += 1

    print(cnt)
    print(f"Processing file: {file_name}")
    print(f"Finished processing file: {file_name}")


files = ["file1.txt", "file2.txt"]  # Список файлов для обработки
# Создание списка асинхронных задач для обработки файлов
for file in files:
    process_file(file)

t2 = time.time()
print(t2 - t1)
