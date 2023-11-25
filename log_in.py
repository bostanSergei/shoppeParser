from playwright.sync_api import sync_playwright
from undetected_playwright import stealth_sync
from fake_useragent import FakeUserAgent
from loguru import logger
import time


# ВНИМАНИЕ! Базовая информация для запуска скрита хранится в файле main.py

# LOGIN - логин пользователя на shopee
# PASSWORD - пароль пользователя на shopee
LOGIN = ''
PASSWORD = ''
URL_MAIN_PAGE = 'https://shopee.co.id/'
URL_LOG_PAGE = 'https://shopee.co.id/buyer/login'


logger.add('debug.log', format="{time} | {level} | {message}")

def log_in_and_save_context() -> None:
    '''Функция открывает страницу для входа в личный кабинет и осуществляет первый поиск. Сразу после
    ввода требуется пройти капчу. Я прохожу её вручную. Далее весь контекст сохраняется в state.json
    и этот контекст используется для дальнейшего поиска.'''
    with sync_playwright() as playwright:
        firefox = playwright.devices["Desktop Firefox"]
        firefox["user_agent"] = FakeUserAgent().firefox
        browser = playwright.firefox.launch(headless=False)
        context = browser.new_context(**firefox, java_script_enabled=True)
        context = stealth_sync(context)
        context.clear_cookies()
        page = context.new_page()

        try:
            logger.info('Процесс авторизации запущен.')
            page.goto('https://shopee.co.id/buyer/login', wait_until="load")

            page.wait_for_timeout(timeout=5000)

            page.keyboard.insert_text(LOGIN)
            page.keyboard.press('Tab')
            page.keyboard.insert_text(PASSWORD)
            page.keyboard.press('Enter')

            page.wait_for_timeout(timeout=10000)
            page.keyboard.press('Escape')
            # через табуляцию дохожу до строки поиска. Других адекватных вариантов не нашел
            for i in range(8):
                page.keyboard.press('Tab')
                time.sleep(2)
            # в качестве первого поиска использую любое ключевое слово. Если не осуществить поиск - не вылезет капча
            # Однако в этом случае она вылезет на этапе первого поиска в основной части програмы.
            for i in 'trash':
                page.keyboard.press(i)
                time.sleep(1)

            page.wait_for_timeout(timeout=10000)
            page.keyboard.press('Enter')

            page.wait_for_timeout(timeout=20000)

            storage = context.storage_state(path='state.json')
            logger.info('Авторизация успешно выполнена')

        except:
            logger.error('Произошла ошибка на этапе авторизации')
            return None

log_in_and_save_context()
