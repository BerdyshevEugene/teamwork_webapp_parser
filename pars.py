import requests
from bs4 import BeautifulSoup
import json

KEYWORDS = ('Python', )  # Можно вынести в конфиг, категории книг!


def get_html(url, params=None):
    try:
        result = requests.get(url, params=params)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return


def get_links_page(html):
    """Парсит ссылки на страницы книг с сайта Piter.com
    :param html:
    :return: Список ссылок с текущей страницы"""
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    all_books = soup.find('div', class_='products-list').find_all('a')
    for link in all_books:
        href = link['href']
        if 'javascript:void(0);' not in href:
            links.append(href)
    return links


def get_all_links_books(category):
    url = 'https://www.piter.com/collection/all'
    page = 1
    books_links = []
    while True:
        params = {
            'q': category, 'page': page, 'page_size': 100
        }
        result = get_html(url, params)
        if result:
            links = get_links_page(result)
            if links:
                books_links.extend(links)
                page += 1
            else:  # Если на странице нет ссылок на книги
                break
    return books_links


if __name__ == '__main__':
    books = {_: {} for _ in KEYWORDS}
    for category in KEYWORDS:
        links = get_all_links_books(category)
        for number, link in enumerate(links, start=1):
            html = get_html('https://www.piter.com' + link)
            soup = BeautifulSoup(html, 'html.parser')

            title = soup.select_one('div[class*="product-info"] > h1').text

            authors_list = []
            authors_html = soup.find('p', class_='author').find_all('span')
            for author in authors_html:
                authors_list.append(author.text)

            year = soup.find('span', string='Год:').find_next_sibling().text.strip()

            publisher = 'Питер'

            price = soup.find('div', string='Цена:')
            if price:
                price = price.find_next_sibling().text.strip()
                price = price.split()[0]

            description = soup.select_one('#tab-1').text

            image_link = soup.find('a', class_='img').find('img')['src']

            isbn = soup.find('span', string='ISBN:').find_next_sibling().text.strip()

            book_info = {
                'title': title,
                'authors': authors_list,
                'year': year,
                'price': price,
                'description': description,
                'image': image_link,
                'isbn': isbn
            }
            books[category][number] = book_info


    # print(books)
    piter_books = {'Питер': books}
    json_dict = json.dumps(piter_books, indent=4)
    # print(json_dict)
    # print(type(json_dict))


    # print(json.loads(json_dict))

    params = {
        'get_json': json_dict
    }

    # requests.post(f'http://127.0.0.1:5000/get-json-books/{json_dict}')

    a = {'asd': 1}

    b = json.dumps(a, indent=4)

    # requests.post(f"http://127.0.0.1:5000/get-json-books/?asd=123")

    cccc = {
      "language": "Python",
      "framework": "Flask",
      "website": "Scotch",
      "version_info": {
        "python": "3.9.0",
        "flask": "1.1.2"
      },
      "examples": ["query", "form", "json"],
      "boolean_test": True
    }

    # requests.post(f"http://127.0.0.1:5000/get-books/", json=cccc)

    ab = 'Популярность Python продолжает расти, а значит, проекты, ' \
         'созданные на этом языке программирования, становятся все масштабнее и сложнее. ' \
         'Многие разработчики проявляют интерес к высокоуровневым паттернам проектирования,' \
         ' таким как чистая и событийно-управляемая архитектура и паттерны предметно-ориентированного проектирования (DDD). ' \
         'Но их адаптация под Python не всегда очевидна. Гарри Персиваль и Боб Грегори познакомят вас с проверенными паттернами, ' \
         'чтобы каждый питонист мог управлять сложностью приложений и получать максимальную отдачу от тестов. ' \
         'Теория подкреплена примерами на чистом Python, лишенном синтаксической избыточности Java и C. ' \
         'В этой книге:•\t«Инверсия зависимостей» и ее связи с портами и адаптерами (гексагональная/чистая архитектура).•\tРазличия между паттернами' \
         ' «Сущность», «Объект-значение» и «Агрегат» в рамках DDD.•\tПаттерны «Репозиторий» и UoW, обеспечивающие постоянство хранения данных.•\tПаттерны «Событие»,' \
         ' «Команда» и «Шина сообщений».•\tРазделение ответственности на команды и запросы (CQRS).•\tСобытийно-управляемая архитектура и реактивные расширения.'


    aaaa = {21: {'title': 'Паттерны разработки на Python: TDD, DDD и событийно-ориентированная архитектура',
                 'authors': ['Персиваль Г.', 'Грегори Б.'], 'year': '2022', 'price': '1045 р.',
                 'description': ab,
                 'iamge': 'https://static-sl.insales.ru/images/products/1/5229/453669997/44611468.jpg', 'isbn': '978-5-4461-1468-9'}}




    # print(json.loads(json_dict))

    # asd = {1: '#'}
    #
    # json_dict = json.dumps(asd, indent=4)
    #
    # requests.post(f"http://127.0.0.1:5000/get-books-try/?key=222&json_dict={json_dict}")

    r = requests.post(
        'http://127.0.0.1:5000/get-books/',
        json=piter_books,
        headers={'Authorization': 'test'},  # TODO: Вынести это в config файл (секретный ключ)
    )

    print(r.json())
