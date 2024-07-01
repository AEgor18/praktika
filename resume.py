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

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '(Promo456)',
    database = 'hh_resume'
)

mycursor = mydb.cursor()
# mycursor.execute('CREATE DATABASE hh_resume')
mycursor.execute("""CREATE TABLE IF NOT EXISTS resume (
                id INTEGER AUTO_INCREMENT PRIMARY KEY,
                position VARCHAR(255),
                experience VARCHAR(255),
                salary INTEGER,
                currency VARCHAR(255),
                last_job VARCHAR(255)
                )""")



def array():
    resume_count = 0
    page = 0
    url = f'https://hh.ru/search/resume?text={text}&exp_period=all_time&logic=normal&pos=full_text&page={page}'
    response = requests.get(url, headers=headers)
    soup = bs(response.text, 'html.parser')
    data = soup.find_all('div', {'class': 'wrapper--eiknuhp1KcZ2hosUJO7g'})
    while resume_count < items:
        for i in data:
            try:
                position = i.find('h3', 'bloko-header-section-3').text
                experience = i.find('div', {'class': 'content--uYCSpLiTsRfIZJe2wiYy'}).text
                salary_str = i.find('div', {'class': 'bloko-text bloko-text_strong'}).text
                currency = salary_str[-2:].replace(' Br', 'BR').replace(' ₽', 'R').replace(' €', 'EU').replace(' ₸', 'T').replace(' $', 'DOL').replace(' ₼', 'AZN')
                salary = salary_str[:-2].replace(' ', '')
                last_job = i.find('span', {'class': 'bloko-text bloko-text_strong'}).text
                yield position, experience, int(salary), currency, last_job
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


# for item in array():
#     position, experience, salary, currency, last_job = item
#     mycursor.execute("INSERT INTO resume (position, experience, salary, currency, last_job) VALUES (%s, %s, %s, %s, %s)",
#                      (position, experience, salary, currency, last_job))
#
# mydb.commit()
# mycursor.execute("ALTER TABLE resume AUTO_INCREMENT = 1")
# mydb.commit()
# mycursor.execute("TRUNCATE TABLE resume")
# mydb.commit()
