from datetime import datetime
from bs4 import BeautifulSoup
from collections import deque
import requests
import logging

logging.basicConfig(filename='sync_links.txt', level=logging.INFO, filemode='w', format='%(asctime)s - %(message)s')


def bfs_wiki(start_url, end_url):
    """
        Алгоритм поиска в ширину
    """
    visited_urls = set()
    queue = deque([(start_url, [])])

    while queue:
        current_url, path = queue.popleft()
        visited_urls.add(current_url)
        page = requests.get(current_url)  # получение страницы
        soup = BeautifulSoup(page.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            url = link['href']
            if url.startswith('/wiki/') and ':' not in url:
                full_url = 'https://ru.wikipedia.org' + url
                if full_url == end_url:
                    # Получение предложения из родительского элемента, не всегда у искомой ссылки есть предложение
                    # например из-за того что ссылка находится в информационном блоке
                    sentence = get_sentence(link.parent.text, link.text)
                    path.append((sentence, full_url))
                    return path
                elif full_url not in visited_urls:
                    logging.info(full_url)
                    sentence = get_sentence(link.parent.text, link.text)
                    queue.append((full_url, path + [(sentence, full_url)]))
                    visited_urls.add(full_url)
        else:
            continue


def print_path(path):
    """
        Выводит в консоль путь до искомой ссылки
    """
    print("Путь:")
    for i, step in enumerate(path, start=1):
        print(i, '-' * 24)
        print(step[0])
        print(step[1])


def get_sentence(text, target):
    """
        Возвращает предложение с искомым словом
    """
    for sentence in text.split('.'):
        if target in sentence:
            return sentence
    return None


def main():
    start_url = input('Введите ссылку от которой начнется поиск(пример: https://ru.wikipedia.org/wiki/Xbox_360_S): ')
    end_url = input('Введите ссылку от которой начнется поиск(пример: https://ru.wikipedia.org/wiki/Nintendo_3DS): ')
    start_time = datetime.now()
    print(f'Старт скрипта {start_time.strftime("%H:%M:%S")}')
    path = bfs_wiki(start_url, end_url)
    print_path(path)
    end_time = datetime.now()
    print('-' * 26)
    print(f'Завершено в {end_time.strftime("%H:%M:%S")}, '
          f'Затраченное время {round((end_time - start_time).total_seconds(), 2)} секунд')


if __name__ == '__main__':
    main()
