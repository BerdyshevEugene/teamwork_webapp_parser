import requests
import json
from bs4 import BeautifulSoup
from requests.api import request

d = input('введите данные для формирования списка книг по тематике: ')
KEYWORDS = ('Python', ) 
# HEADERS = {'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.8.0.1716 Yowser/2.5 Safari/537.36', 'accept': '*/*'}
books = []
links = []
HOST = 'https://www.piter.com'
FILE = 'books.json'


def get_html(url, params=None):
    try:
        result = requests.get(url, params=params)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('div', class_='pagination right clear').find_all('a', href=True)
    if pagination:
        return int (pagination[-2].get_text())
    else:
        return 1


def get_links_page(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    all_books = soup.find('div', class_='products-list').find_all('a')
    for link in all_books:
        href = link['href']
        if 'javascript:void(0);' not in href:
            links.append(href)
    return links


def get_all_links_books(category):
    url = 'https://www.piter.com/collection/all?q='+(d)+'&r46_search_query='+(d)+'&r46_input_query='+(d)
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
    piter_books = {_: {} for _ in KEYWORDS}
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

            description = soup.select_one('#tab-1').text

            image_link = soup.find('a', class_='img').find('img')['src']

            isbn = soup.find('span', string='ISBN:').find_next_sibling().text.strip()

            book_info = {
                'title': title,
                'authors': authors_list,
                'year': year,
                'publisher': 'Питер',
                'price': price,
                'description': description,
                'category': category,
                'image': image_link,
                'isbn': isbn
            }
            piter_books[category][number] = book_info

    print(piter_books)

    with open('piter_books.json', 'w', encoding='utf-8') as file:
        json.dump(piter_books, file, indent=2, ensure_ascii=False)