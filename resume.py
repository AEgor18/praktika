from bs4 import BeautifulSoup as bs
import requests


text = 'python'
items = 20
headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Yandex',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br'
}
count = 0

def get_url(page):
    url = f'https://hh.ru/search/resume?text={text}&no_magic=true&ored_clusters=true&order_by=relevance&items_on_page={items}&search_period=0&logic=normal&pos=full_text&exp_period=all_time&page={page}'
    response = requests.get(url, headers=headers)
    soup = bs(response.text, 'html.parser')
    data = soup.find_all('div', {'class': 'wrapper--eiknuhp1KcZ2hosUJO7g'})
    for i in data:
        card_url = 'https://hh.ru' + i.find('a').get('href')
        yield card_url


def array():
    global count
    page = 1
    while count < items:
        for card_url in get_url(page):
            try:
                response = requests.get(card_url, headers=headers)
                soup = bs(response.text, 'html.parser')
                data = soup.find('div', {'class': 'bloko-gap bloko-gap_top'})
                if data:
                    position = data.find('h2', {'class': 'bloko-header-2'}).text
                    specialization = data.find('li', {'class': 'resume-block__specialization'}).text
                    employment = data.find('div', {'resume-block-container'}).find('p').text.replace('Занятость: ', '')
                    #gender = data.find('div', {'class': 'resume-header-title'}).find('span').text
                    print(position)
                    count += 1
                    if count >= items:
                        break
            except:
                pass
        page += 1

array()