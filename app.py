from flask import Flask, render_template, request, jsonify
import mysql.connector
from bs4 import BeautifulSoup as bs
import requests

app = Flask(__name__)

# Настройки базы данных
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='(Promo456)',
    database='hh_resume'
)

mycursor = mydb.cursor()
mycursor.execute("ALTER TABLE resume AUTO_INCREMENT = 1")
mycursor.execute("TRUNCATE TABLE resume")
mydb.commit()
def parse_resumes(text, items=50):
    headers = {
        'Host': 'hh.ru',
        'User-Agent': 'Yandex',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    resume_count = 0
    page = 0
    while resume_count < items:
        url = f'https://hh.ru/search/resume?text={text}&exp_period=all_time&logic=normal&pos=full_text&page={page}'
        response = requests.get(url, headers=headers)
        soup = bs(response.text, 'html.parser')
        data = soup.find_all('div', {'class': 'wrapper--eiknuhp1KcZ2hosUJO7g'})
        for i in data:
            try:
                position = i.find('a', 'bloko-link').text
                experience = i.find('div', {'class': 'content--uYCSpLiTsRfIZJe2wiYy'}).text.replace(' ', ' ')
                salary_str = i.find('div', {'class': 'bloko-text bloko-text_strong'}).text
                currency = salary_str[-2:]
                salary = salary_str[:-2].replace(' ', '')
                last_job = i.find('span', {'class': 'bloko-text bloko-text_strong'}).text
                mycursor.execute("INSERT INTO resume (position, experience, salary, currency, last_job) VALUES (%s, %s, %s, %s, %s)",
                                 (position, experience, int(salary), currency, last_job))
                mydb.commit()
                resume_count += 1
                if resume_count >= items:
                    break
            except:
                pass
        page += 1

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        parse_resumes(text)
        mycursor.execute("SELECT * FROM resume WHERE position LIKE %s", ('%' + text + '%',))
        resumes = mycursor.fetchall()
        return render_template('index.html', resumes=resumes, text=text)
    else:
        mycursor.execute("SELECT * FROM resume")
        resumes = mycursor.fetchall()
    return render_template('index.html', resumes=resumes)

if __name__ == '__main__':
    app.run(debug=True)
