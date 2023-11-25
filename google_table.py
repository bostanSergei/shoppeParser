from oauth2client.service_account import ServiceAccountCredentials
import gspread
import datetime
from loguru import logger


# ВНИМАНИЕ! Базовая информация для запуска скрита хранится в файле main.py

logger.add('debug.log', format="{time} | {level} | {message}")

# FILE_WITH_API_KEYS - JSON c ключами для доступа к Google - таблице (по умолчанию в корневом каталоге)
# TABLE_NAME_FOR_UPDATE - имя таблицы в гугл документах (не забыть дать доступ к таблице) в которую грузим результаты
# TABLE_NAME_FOR_READ - имя таблицы в гугл документах (не забыть дать доступ к таблице) из которой забираем ключи и ссылки
FILE_WITH_API_KEYS = 'credentials.json'
TABLE_NAME_FOR_UPDATE = 'shoppeTable'
TABLE_NAME_FOR_READ = 'shope-search-in'

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


def update_data(result_data: dict, key_word: str) -> None:
    data_to_update = [
        [f'{datetime.datetime.today()}',
         key_word,
         key,
         " | ".join(map(str, val)) if len(val) > 1 else val[0] if len(val) == 1 else 0]
        for key, val in result_data.items()
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(FILE_WITH_API_KEYS, SCOPE)
    gc = gspread.authorize(credentials)

    spreadsheet = gc.open(TABLE_NAME_FOR_UPDATE)
    worksheet = spreadsheet.get_worksheet(0)
    worksheet.append_rows(data_to_update)

    logger.info(f'Результаты по ключу {key_word} в таблицу добавлены')


def get_data(table_name: str = TABLE_NAME_FOR_READ) -> dict:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(FILE_WITH_API_KEYS, SCOPE)
    gc = gspread.authorize(credentials)

    spreadsheet = gc.open(table_name)
    worksheet = spreadsheet.get_worksheet(0)

    data_from_table = worksheet.get_all_values()

    resutDict = {}

    for key, url in data_from_table[1:]:
        if key not in resutDict:
            resutDict[key] = []

        index = url.find('?')
        value = url[:index]

        resutDict[key].append(value)

    logger.info(f'Загружены все ключи и ссылки из указанной таблицы')
    return resutDict
