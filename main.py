from bs4 import BeautifulSoup as bs
import requests

headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Yandex'
}
url = 'https://hh.ru/search/vacancy?text=python&items_on_page=100'
request = requests.get(url, headers=headers)
# print(request.status_code)
soup = bs(request.text, 'html.parser')
# paginator = soup.find('span', {'class': ''})
