import asyncio
import time

t1 = time.time()


async def process_file(file_name):
    f = open(file_name)
    cnt = 0
    for symb in f.read():
        if symb == "a":
            cnt += 1

    print(cnt)
    print(f"Processing file: {file_name}")
    print(f"Finished processing file: {file_name}")


async def main():
    files = ["file1.txt", "file2.txt"]  # Список файлов для обработки

    # Создание списка асинхронных задач для обработки файлов
    tasks = [process_file(file) for file in files]

    # Запуск всех задач асинхронно
    await asyncio.gather(*tasks)


# Запуск основной программы
asyncio.run(main())
t2 = time.time()
print(t2 - t1)
