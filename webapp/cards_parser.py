import requests
import json
from bs4 import BeautifulSoup
from requests.api import request

list_url = []
cards_books = []


def get_html(list_url, params=None):
    r = requests.get(list_url, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='grid-4 m-grid-7 s-grid-12 product-info'). find_all('div')
    for item in items:
        title = item.find('h1')
        # author = item.find('span', {'class': 'author'})
        # price = item.find('span', {'class': 'price'})
        # url = item.find('a', href=True)
        if None in (title):
            continue
        cards_books.append({
            'title': title.text.strip()
            # 'author': author.text.strip(),
            # 'price': price.text.strip(),
            # 'url': HOST + url['href']
        })
    with open('cards_books.json', 'w', encoding='utf-8') as file:
        json.dump(cards_books, file, indent=2, ensure_ascii=False)
    return cards_books

def parse():
    path = 'books.json'
    with open(path, 'r') as file:
        data = json.loads(file.read())
        for url in data:
            list_url.append([url['url']])
    html = get_html(list_url)
    if html.status_code == 200:
        cards_books = []
        cards_books.extend(get_content(html.text))



if __name__ == "__main__":
    parse()
    get_content()




# def url_list():
#     path = 'books.json'
#     with open(path, 'r') as file:
#         data = json.loads(file.read())
#         for url in data:
#             list_url.append([url['url']])
#             print(list_url)
#     get_content(list_url)