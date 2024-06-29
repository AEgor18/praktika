from bs4 import BeautifulSoup as bs
import requests

text = 'python'

headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Yandex',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br'
}
url = f'https://hh.ru/search/vacancy?&text={text}'
def hh():
    request = requests.get(url, headers=headers)
    # print(request.status_code)
    # print(request.text)
    soup = bs(request.text, 'lxml')
    paginator = soup.find_all('span', {'class': 'pager-item-not-in-short-range'})
    pages=[]
    for page in paginator:
        pages.append(int(page.find('a').text))

    return pages[-1]

max_page = hh()

def hh_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f'{url}&page={page}', headers=headers)
        # print(result.status_code)
        soup = bs(result.text, 'lxml')
        results = soup.find_all('div',  {'class': 'vacancy-search-item__card'})
        for result in results:
            try:
                title = result.find('a').text
                company = result.find('span', {'class': 'company-info-text--vgvZouLtf8jwBmaD1xgp'}).text
                experience = result.find('span', {'class': 'label--rWRLMsbliNlu_OMkM_D3'}).text
                city = result.find('div', {'class': 'info-section--N695JG77kqwzxWAnSePt'}).find('div', {'class': 'wide-container--lnYNwDTY2HXOzvtbTaHf'}).find('span').text
                salary = result.find('span', {'class': 'bloko-text'}).find('span', {'class': 'fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni'}).text
                print(title, company, experience, city, salary)
            except:
                pass
hh_jobs(max_page)