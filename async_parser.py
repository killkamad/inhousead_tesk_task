from datetime import datetime
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import logging

logging.basicConfig(filename='async_links.txt', level=logging.INFO, filemode='w', format='%(asctime)s - %(message)s')


async def bfs_wiki(start_url, end_url):
    """
        Алгоритм поиска в ширину
    """
    visited_urls = set()
    queue = asyncio.Queue()
    await queue.put((start_url, []))

    while queue:
        current_url, path = await queue.get()
        visited_urls.add(current_url)
        html = await get_page_html(current_url)  # получение html страницы
        soup = BeautifulSoup(html, 'html.parser')
        all_a_tags = soup.find_all('a', href=True)
        for link in all_a_tags:
            url = link['href']
            if url.startswith('/wiki/') and ':' not in url:
                full_url = 'https://ru.wikipedia.org' + url
                if full_url == end_url:
                    # Получение предложения из родительского элемента, не всегда у искомой ссылки есть предложение
                    # например из-за того что ссылка находится в информационном блоке
                    sentence = await get_sentence(link.parent.text, link.text)
                    path.append((sentence, full_url))
                    return path
                elif full_url not in visited_urls:
                    logging.info(full_url)
                    sentence = await get_sentence(link.parent.text, link.text)
                    await queue.put((full_url, path + [(sentence, full_url)]))
                    visited_urls.add(full_url)
        else:
            continue


async def get_page_html(url):
    """
        Получение html текста страницы
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def print_path(path):
    """
        Выводит в консоль путь до искомой ссылки
    """
    print("Путь:")
    for i, step in enumerate(path, start=1):
        print(i, '-' * 24)
        print(step[0])
        print(step[1])


async def get_sentence(text, target):
    """
        Возвращает предложение с искомым словом
    """
    for sentence in text.split('.'):
        if target in sentence:
            return sentence
    return None


async def main():
    """
        Главная функция с вызовом алгоритма поиска в ширину
    """
    start_url = input('Введите ссылку от которой начнется поиск(пример: https://ru.wikipedia.org/wiki/Xbox_360_S): ')
    end_url = input('Введите ссылку от которой начнется поиск(пример: https://ru.wikipedia.org/wiki/Nintendo_3DS): ')
    start_time = datetime.now()
    print(f'Старт скрипта {start_time.strftime("%H:%M:%S")}')
    path = await bfs_wiki(start_url, end_url)
    await print_path(path)
    end_time = datetime.now()
    print('-' * 26)
    print(f'Завершено в {end_time.strftime("%H:%M:%S")}, '
          f'Затраченное время {round((end_time - start_time).total_seconds(), 2)} секунд')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
