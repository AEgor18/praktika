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

list_card_url = []
# def get_url():
for page in range(1):
    request = requests.get(f'{url}&page={page}', headers=headers)
    soup = bs(request.text, 'lxml')
    data = soup.find_all('div',  {'class': 'vacancy-search-item__card'})
    for i in data:
        card_url = i.find('a').get('href')
        list_card_url.append(card_url)

for card_url in  list_card_url:
    response = requests.get(card_url, headers=headers)
    soup = bs(response.text, 'lxml')
    data = soup.find('div', {'class': 'wrapper-flat--H4DVL_qLjKLCo1sytcNI'})
    data1 = soup.find('div', {'class': 'vacancy-company-redesigned'})
    if data != None:
        try:
            title = data.find('h1', {'class': 'bloko-header-section-1'}).text
            salary = data.find('span', {'class': 'magritte-text___pbpft_3-0-9 magritte-text_style-primary___AQ7MW_3-0-9 magritte-text_typography-label-1-regular___pi3R-_3-0-9'}).text
            description = data.find_all('p', {'class': 'vacancy-description-list-item'})
            experience = description[0].text
            busyness = description[1].text
            company = data1.find('span', {'class': 'bloko-header-section-2 bloko-header-section-2_lite'}).text
            address = data1.find('div', {'class': 'magritte-text___pbpft_3-0-9 magritte-text_style-primary___AQ7MW_3-0-9 magritte-text_typography-paragraph-2-regular___VO638_3-0-9'}).text
            print(title, salary, experience,  busyness, company, address)
        except:
            print(title, salary, experience,  busyness, company, 'Адрес не указан')



