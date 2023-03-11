# Парсер википедии

## Инструкция для запуска:

1. Настройка виртуального окружения

   1.1 Создать и активировать виртуальное окружение

    ```bash
   # Windows:
    python -m venv venv
   .\venv\Scripts\activate
   
   # Linux:
   virtualenv -p python3.8 .venv
   source .venv/bin/activate
    ```
   1.2 Установка необходимых библиотек

    ```bash
    pip install -r requirements.txt
    ```

2. Запустить `async_parser.py` или `sync_parser.py`, Пример:

   ```bash
    python async_parser.py
    ```

3. Парсер запросит две ссылки, начало поиска и конец поиска. Например.

   ```bash
   Введите ссылку от которой начнется поиск(пример: https://ru.wikipedia.org/wiki/Xbox_360_S): https://ru.wikipedia.org/wiki/Xbox_360_S
   Введите ссылку от которой начнется поиск(пример: https://ru.wikipedia.org/wiki/Nintendo_3DS): https://ru.wikipedia.org/wiki/RadioShack
    ```
   Время выполнения для примера из тестового задания примерно +- 2 секунды