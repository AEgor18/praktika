import mysql.connector
from bs4 import BeautifulSoup as bs
import requests
import time

text = input()
items = 50
max_pages = 5  # Максимальное количество страниц для просмотра
headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Yandex',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br'
}

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='(Promo456)',
    database='hh_resume'
)

mycursor = mydb.cursor(buffered=True)  # Использование buffered=True

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
    session = requests.Session()  # Использование requests.Session()
    while resume_count < items and page < max_pages:
        url = f'https://hh.ru/search/resume?text={text}&exp_period=all_time&logic=normal&pos=full_text&page={page}'
        response = session.get(url, headers=headers)  # Использование session
        soup = bs(response.text, 'lxml')
        data = soup.select('div.wrapper--eiknuhp1KcZ2hosUJO7g')  # Использование soup.select()
        time.sleep(0.2)  # Пауза между запросами

        for i in data:
            try:
                position = i.select_one('a.bloko-link').text  # Использование select_one()
                experience = i.select_one('div.content--uYCSpLiTsRfIZJe2wiYy').text.replace(' ', ' ')
                salary_str = i.select_one('div.bloko-text.bloko-text_strong').text
                currency = salary_str[-2:].replace(' Br', 'BR').replace(' ₽', 'R').replace(' €', 'EU').replace(' ₸', 'T').replace(' $', 'DOL').replace(' ₼', 'AZN')
                salary = salary_str[:-2].replace(' ', '')
                last_job = i.select_one('span.bloko-text.bloko-text_strong').text
                yield position, experience, int(salary), currency, last_job
                resume_count += 1
                if resume_count >= items:
                    break
            except:
                pass

        page += 1

mycursor.execute("ALTER TABLE resume AUTO_INCREMENT = 1")
mycursor.execute("TRUNCATE TABLE resume")
mydb.commit()

data_to_insert = list(array())
mycursor.executemany(
    "INSERT INTO resume (position, experience, salary, currency, last_job) VALUES (%s, %s, %s, %s, %s)",
    data_to_insert
)  # Использование executemany()

mydb.commit()

mycursor.execute('SELECT * FROM resume')
myresult = mycursor.fetchall()
for row in myresult:
    print(row)