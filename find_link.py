from bs4 import BeautifulSoup


# ВНИМАНИЕ! Базовая информация для запуска скрита хранится в файле main.py

def get_pagination_page(text: str) -> int | None:
    '''Получаем последнюю страницу пагинации. Вообще, в процессе тестов выяснилось, что эта функция особо
    не нужна (по крайней мере по тем ключевым словам, которые принимали участие в тестировании), однако
    если доступных страниц будет меньше - через функцию получим крайнюю'''
    soup = BeautifulSoup(text, 'lxml')
    lastPage = None
    result = soup.find('div', 'shopee-mini-page-controller__state')

    if result:
        lastPage = result.text.split('/')
        if len(lastPage) > 1 and lastPage[-1].isdigit():
            return int(lastPage[-1])

    return lastPage


def find_link_on_page(text: str) -> list:
    '''Поиск ссылок всех товаров на странице. С каждой ссылки сразу убираем рандомный хвост и возвращем
    список "чистых" ссылок'''
    soup = BeautifulSoup(text, 'lxml')

    result = soup.find_all('div', 'shopee-search-item-result__item')

    productLinks = []
    if result:
        for tag in result:
            productLinks.append(tag.find_next('a')['href'])

    productLinks = [link[1:link.index('?')] for link in productLinks]

    return productLinks


# with open('file.txt', 'r', encoding='utf-8') as htmlFile:
#     txt = htmlFile.read()
#     print(pagination_page(txt))
#     print()
#     print(find_link_on_page(txt))
