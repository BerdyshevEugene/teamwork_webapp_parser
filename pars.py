import requests
from bs4 import BeautifulSoup

KEYWORDS = ('Python', 'JavaScript', 'Java')  # Можно вынести в конфиг, категории книг!


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

    piter_books = {'Питер': books}

    r = requests.post(
        'http://127.0.0.1:5000/get-books/',
        json=piter_books,
        headers={'Authorization': 'test'},  # TODO: Вынести это в config файл (секретный ключ)
    )
    print(r.json())
