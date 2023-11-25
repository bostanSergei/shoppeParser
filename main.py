from log_in import log_in_and_save_context
from google_table import get_data, update_data
from by_keywords import open_session
import time


# ВНИМАНИЕ! Перед запуском скрипта требуется скачать со своего личного кабинета JSON с ключами для доступа к
# google API. В коревом каталоге должен лежать файл credentials.json
# Так же на своем гугл диске необходимо создать таблицы: в первой будут храниться ключевые слова и ссылки на товары
# во вторую - будут писаться результаты работы очередного запуска.
# Имена этих таблиц можно изменить в файле google_table.py
# Так же в файле log_in.py ввести свой логин и пароль от личного кабинета на shoppe


def main():
    # логинимся и сохраняем контекст
    log_in_and_save_context()
    time.sleep(10)

    # грузим данные из гугл таблицы с ключевыми словами и ссылками
    key_word_and_link_dict = get_data()

    # обрабатываем каждое ключевое слово и записываем результаты в гугл таблицу
    for key, url_list in key_word_and_link_dict.items():
        resultData, key_word = open_session(key, url_list)

        update_data(resultData, key_word)


if __name__ == "__main__":
    main()
