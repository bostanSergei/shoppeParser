from find_link import get_pagination_page, find_link_on_page
from playwright.sync_api import sync_playwright
from loguru import logger
import time


# ВНИМАНИЕ! Базовая информация для запуска скрита хранится в файле main.py

logger.add('debug.log', format="{time} | {level} | {message}")

# список ниже был создан для проверки парсинга. Важно было понять: действительно ли при парсинге я получаю
# все ссылки. При пагинации по всем страницам мы должны были получить 1020 ссылок (17 * 60).
# Теория подтвердилась!
# allLinks = []


def open_session(key_word: str, list_link: list, maximum_product: int = 500) -> tuple:
    '''Открываем сессию для поиска. Каждая сессия - это новое ключевое слово и список ссылок, которые будем искать.
    maximum_product - ограничение поиска (по умолчанию 500), то есть по факту задача просмотреть первые 9 страниц.
    На каждой странице по 60 товаров. Если на этих страницах товар не найден - вернем 0 в качестве результата'''

    key_for_logger = key_word
    key_word = 'search?keyword=' + key_word
    url = 'https://shopee.co.id/' + key_word

    placeIndexDict = {link: [] for link in list_link}

    def findList(links_in_page: list, page_number: int) -> None:
        '''Функция принимает список ссылок с текущей страницы и ищет совпадения'''
        # allLinks.extend(links_in_page)
        for index in range(len(links_in_page)):
            if links_in_page[index] in placeIndexDict:
                logger.info(f'Найден товар на странице {page_number + 1} | ПОЗИЦИЯ ТОВАРА | {page_number * 60 + (index + 1)} | ССЫЛКА НА ТОВАР | {links_in_page[index]}')

                # при тестах заметил вот какую особенность: товар находиться на разных позициях. Так к примеру было
                # с товаром Dawndesslo-Tempat-Sampah-Mobil-Trash-Bin-Pressing-Type-DDE301-i.192060959.13674988338
                # он был сначала найден на странице 1, в потом на странице 17. Чтобы значение не перезаписывалось
                # решил добавить сделать список, в который добавляем нвоое значение

                placeIndexDict[links_in_page[index]].append(page_number * 60 + (index + 1))

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=True)
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()

        logger.info(f'Старт поиска | {key_for_logger} | FIRST PAGE')

        page.goto(url, wait_until="load")

        page.wait_for_timeout(timeout=10000)

        for i in range(10):
            page.keyboard.press('PageDown')
            time.sleep(2)

        text = page.content()

        lastPage = get_pagination_page(text)
        linksInPage = find_link_on_page(text)
        k = 0

        findList(linksInPage, k)

        for j in range(1, lastPage):
            logger.info(f'Переход на страницу | {j + 1}')

            paginationUrl = url + f'&page={j}'
            page.goto(paginationUrl, wait_until='load')

            page.wait_for_timeout(timeout=10000)

            for i in range(6):
                page.keyboard.press('PageDown')
                time.sleep(1)

            text = page.content()
            linksInPage = find_link_on_page(text)

            findList(linksInPage, j)

            if j >= maximum_product // 60:
                logger.info('Поиск по ключевому слову закончен | Превышено органичение по количеству товаров')
                return placeIndexDict, key_for_logger

            elif any([value == [] for value in placeIndexDict.values()]):
                continue

            else:
                logger.info('Поиск по ключевому слову закончен. | Найдены все товары по ключевому слову')
                return placeIndexDict, key_for_logger

        logger.info('Поиск по ключевому слову закончен. | Пройдены все доступные для пагинации страницы')
        return placeIndexDict, key_for_logger
