import mysql.connector
from bs4 import BeautifulSoup as bs
import requests

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '(Promo456)',
    database = 'vacancies'
)

mycursor = mydb.cursor()
mycursor.execute("""CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER AUTO_INCREMENT PRIMARY KEY,
                position VARCHAR(255),
                company VARCHAR(255),
                experience VARCHAR(255),
                salary VARCHAR(255),
                schedule VARCHAR(255),
                address VARCHAR(255)
                )""")

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


def get_url():
    for page in range(max_page):
        request = requests.get(f'{url}&page={page}', headers=headers)
        soup = bs(request.text, 'lxml')
        data = soup.find_all('div',  {'class': 'vacancy-search-item__card'})
        for i in data:
            card_url = i.find('a').get('href')
            yield card_url


def array():
    for card_url in get_url():
        response = requests.get(card_url, headers=headers)
        soup = bs(response.text, 'lxml')
        data = soup.find('div', {'class': 'wrapper-flat--H4DVL_qLjKLCo1sytcNI'})
        data1 = soup.find('div', {'class': 'vacancy-company-redesigned'})
        if data:
            position = data.find('h1', {'class': 'bloko-header-section-1'}).text
            company = data1.find('span', {'class': 'bloko-header-section-2 bloko-header-section-2_lite'}).text
            description = data.find_all('p', {'class': 'vacancy-description-list-item'})
            experience = description[0].text.replace("Требуемый опыт работы ", "")
            salary = data.find('span', {'class': 'magritte-text___pbpft_3-0-9 magritte-text_style-primary___AQ7MW_3-0-9 magritte-text_typography-label-1-regular___pi3R-_3-0-9'}).text
            schedule1 = description[1].text
            parts = schedule1.split(', ')
            schedule = parts[0]
            employment = parts[1] if len(parts) > 1 else None
            address_element = data1.find('div', {
                'class': 'magritte-text___pbpft_3-0-9 magritte-text_style-primary___AQ7MW_3-0-9 magritte-text_typography-paragraph-2-regular___VO638_3-0-9'})
            address = address_element.find('p').text if address_element else None
            if address is None:
                address1_element = data1.find('span', {'class': 'magritte-text___tkzIl_4-1-4'})
                address = address1_element.find('span').text if address1_element else None
            yield position, company, experience.replace('Требуемый опыт работы:', ''), salary, schedule, address

# for item in array():
#     position, company, experience, salary, schedule, address = item
#     mycursor.execute("INSERT INTO vacancies (position, company, experience, salary, schedule, address) VALUES (%s, %s, %s, %s, %s, %s)",
#                    (position, company, experience, salary, schedule, address))
mycursor.execute("DELETE FROM vacancies")
mydb.commit()