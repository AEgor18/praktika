from bs4 import BeautifulSoup as bs
import requests


text = 'c++'
items = 5
headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Yandex',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br'
}


def get_url(page):
    url = f'https://hh.ru/search/resume?text={text}&no_magic=true&ored_clusters=true&order_by=relevance&items_on_page={items}&search_period=0&logic=normal&pos=full_text&exp_period=all_time&page={page}'
    response = requests.get(url, headers=headers)
    soup = bs(response.text, 'lxml')
    data = soup.find_all('div', {'class': 'wrapper--eiknuhp1KcZ2hosUJO7g'})
    for i in data:
        card_url = 'https://hh.ru' + i.find('a').get('href')
        yield card_url

def array():
    resume_count = 0
    page = 0
    while resume_count < items:
        try:
            for card_url in get_url(page):
                response = requests.get(card_url, headers=headers)
                soup = bs(response.text, 'lxml')
                data = soup.find('div', {'class': 'resume-header-main'})
                data1 = soup.find('div', {'class': 'resume-block'})
                data2 = soup.find('h2', {'class': 'bloko-header-2 bloko-header-2_lite'})
                if data:
                    dannie = data.find('p').text
                    parts = dannie.split(', ')
                    gender = parts[0]
                    age = parts[1] if len(parts) > 1 else 'Не указан'
                    position = data1.find('span', {'class': 'resume-block__title-text'}).text
                    specialization = data1.find('li', {'class': 'resume-block__specialization'}).text
                    employment1 = data1.find('div', {'class': 'resume-block-container'}).text
                    parts1 = employment1.split(': ')
                    employment = parts1[1].replace('График работы', '')
                    schedule = parts1[2]
                    #experience = data2.find('span', {'class': 'resume-block__title-text resume-block__title-text_sub'}).text.replace('Опыт работы ', '')
                    print(position, specialization, gender, age, employment, schedule)
                    #print(experience)
                resume_count += 1
                if resume_count >= items:
                    break
        except:
            pass
array()


