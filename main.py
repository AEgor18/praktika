from bs4 import BeautifulSoup as bs
import requests

text = 'python'
items = 100

headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Yandex'
}
url = f'https://hh.ru/search/vacancy?&text={text}&items_on_page={items}'
def hh():
    request = requests.get(url, headers=headers)
    # print(request.status_code)
    soup = bs(request.text, 'html.parser')
    paginator = soup.find_all('span', {'class': 'pager-item-not-in-short-range'})

    pages=[]

    for page in paginator:
        pages.append(int(page.find('a').text))

    return pages[-1]

max_page = hh()

def hh_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f'{url}&page=0', headers=headers)
        # print(result.status_code)
        soup = bs(result.text, 'html.parser')
        results = soup.find_all('div',  {'class': 'vacancy-search-item__card'})
        for result in results:
            title = result.find('a').text
            company = result.find('div', {'class': 'info-section--N695JG77kqwzxWAnSePt'}).find('span').text
            print(title, company)

    return title
hh_jobs(max_page)