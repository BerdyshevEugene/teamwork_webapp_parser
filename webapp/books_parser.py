import requests
import json
from bs4 import BeautifulSoup
from requests.api import request

d = input ('введите данные для формирования списка книг по тематике: ')
URL=('https://www.piter.com/collection/all?q='+(d)+'&r46_search_query=дети&r46_input_query='+(d))
HEADERS = {'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.8.0.1716 Yowser/2.5 Safari/537.36', 'accept': '*/*'}
list_of_books = []
HOST = 'https://www.piter.com'
FILE = 'books.json'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('div', class_='pagination right clear').find_all('a', href=True)
    if pagination:
        return int (pagination[-2].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='products-list'). find_all('div')
    books = []
    for item in items:
        title = item.find('span', {'class': 'title'})
        author = item.find('span', {'class': 'author'})
        price = item.find('span', {'class': 'price'})
        url = item.find('a', href=True)
        if None in (title, author, price, url):
            continue
        books.append({
            'title': title.text.strip(),
            'author': author.text.strip(),
            'price': price.text.strip(),
            'url': HOST + url['href']
        })
        with open ('books.json', 'w', encoding='utf-8') as file:
            json.dump(books, file, indent=2, ensure_ascii=False)
    return books


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        books = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            books.extend(get_content(html.text))
        print(f'получено {len (books)} книг')
    else:
        print('Ошибка. По запросу нет данных.')



parse()