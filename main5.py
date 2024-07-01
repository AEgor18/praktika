import mysql.connector
from bs4 import BeautifulSoup as bs
import requests

text = 'курьер'
items = 20
headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Yandex',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br'
}

def get_url(page):
    url = f'https://hh.ru/search/resume?exp_period=all_time&logic=normal&no_magic=true&order_by=relevance&ored_clusters=true&pos=full_text&search_period=0&text={text}&items_on_page=100&page={page}'
    response = requests.get(url, headers=headers)
    soup = bs(response.text, 'lxml')
    data = soup.find_all('div', {'class': 'wrapper--eiknuhp1KcZ2hosUJO7g'})
    for i in data:
        card_url = 'https://hh.ru' + i.find('a').get('href')
        yield card_url

def array():
    vacancy_count = 0
    page = 0
    while vacancy_count < items:
        try:
            for card_url in get_url(page):
                response = requests.get(card_url, headers=headers)
                soup = bs(response.text, 'lxml')
                data = soup.find('div', {'class': 'resume-applicant'})
                if data:
                    position = data.find('h2', {'class': 'bloko-header-2'}).text
                    specialization = 'Не указано' if data.find('li', {
                        'class': 'resume-block__specialization'}) is None else data.find('li', {
                        'class': 'resume-block__specialization'}).text
                    experience = data.find('span', {'class': 'resume-block__title-text resume-block__title-text_sub'}).text.replace('Опыт работы ', '')
                    gender1 = data.find('div', {'class': 'resume-header-title'}).find('p').text
                    parts = gender1.split(', ')
                    gender = parts[0]
                    age = parts[1].replace('года', '').replace('год', '').replace('лет', '')
                    employment1 = data.find('div', {'class': 'resume-block-container'}).text
                    parts1 = employment1.split(':')
                    employment = parts1[2].replace('График работы', '')
                    schedule = parts1[3]
                    print(position, specialization, experience, gender, age, employment, schedule)
                    # print(position, specialization)
                    vacancy_count += 1
                    if vacancy_count >= items:
                        break
            page += 1
        except:
            pass

array()