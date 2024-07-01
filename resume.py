import mysql.connector
from bs4 import BeautifulSoup as bs
import requests

text = 'python'
items = 50
headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Yandex',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br'
}



def array():
    resume_count = 0
    page = 0

    url = f'https://hh.ru/search/resume?text={text}&exp_period=all_time&logic=normal&pos=full_text&page={page}'
    response = requests.get(url, headers=headers)
    soup = bs(response.text, 'lxml')
    data = soup.find_all('div', {'class': 'wrapper--eiknuhp1KcZ2hosUJO7g'})
    while resume_count < items:
        for i in data:
            try:
                position = i.find('h3', 'bloko-header-section-3').text
                experience = i.find('div', {'class': 'content--uYCSpLiTsRfIZJe2wiYy'}).text
                salary = i.find('div', {'class': 'bloko-text bloko-text_strong'}).text
                last_job = i.find('span', {'class': 'bloko-text bloko-text_strong'}).text
                print(position, experience, salary, last_job)
                resume_count += 1
                if resume_count >= items:
                    break
            except:
                pass

        page += 1
        url = f'https://hh.ru/search/resume?text={text}&exp_period=all_time&logic=normal&pos=full_text&page={page}'
        response = requests.get(url, headers=headers)
        soup = bs(response.text, 'lxml')
        data = soup.find_all('div', {'class': 'wrapper--eiknuhp1KcZ2hosUJO7g'})
