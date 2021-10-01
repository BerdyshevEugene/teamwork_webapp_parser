import requests
from bs4 import BeautifulSoup
list_of_books = []

for python_books_all in range(1):
    url = 'https://www.piter.com/collection/all?page_size=100&order=&q=python&only_available=true'
    par = {'p': python_books_all}
    r = requests.get(url, params=par)
    soup = BeautifulSoup(r.text, 'html.parser') 
    for book in range(44):
        title = soup.find_all('span', class_="title")[book].get_text()
        url = soup.find_all('a')[book]['href']
        url = 'https://www.piter.com' + url
        list_of_books.append([title, url])
with open ('/Users/macbook/PythonProjects/LPproject/teamwork_webapp_parser/books.csv', 'w', encoding='utf-8') as out:
    for book in list_of_books:
        book=str(book)
        book=book.replace('\"', '')
        book=book.replace('[', '')
        book=book.replace(']', '')
        out.write(book + '\n')
