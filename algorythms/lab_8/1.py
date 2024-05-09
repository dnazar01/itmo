import asyncio
import aiohttp


async def fetch_page(url, session):
    async with session.get(url) as response:
        return await response.text()


async def main():
    urls = [
        "https://ya.ru/",
        "https://google.com",
        "https://ru.wikipedia.org/wiki/Заглавная_страница",
    ]

    async with aiohttp.ClientSession() as session:
        # Создаем список асинхронных задач для загрузки каждой веб-страницы
        tasks = [fetch_page(url, session) for url in urls]

        # Запускаем все задачи асинхронно
        pages = await asyncio.gather(*tasks)

        # Выводим результаты загрузки каждой веб-страницы
        for url, page in zip(urls, pages):
            print(
                f"Page from {url}:\n{page[:100]}...'\n\n\n"
            )  # Выводим только первые 100 символов


# Запуск основной программыw
asyncio.run(main())
