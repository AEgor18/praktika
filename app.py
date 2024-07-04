from flask import Flask, render_template, request, jsonify, url_for, redirect
import mysql.connector
from bs4 import BeautifulSoup as bs
import requests

app = Flask(__name__)

headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Yandex',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br'
}

mydb_resume = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='(Promo456)',
    database='hh_resume'
)

mydb_vacancy = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='(Promo456)',
    database='vacancies_hh'
)

mycursor_resume = mydb_resume.cursor()
mycursor_vacancy = mydb_vacancy.cursor()
mycursor_vacancy.execute("TRUNCATE TABLE hh_vacancies2")
mycursor_vacancy.execute("ALTER TABLE hh_vacancies2 AUTO_INCREMENT = 1")
mydb_vacancy.commit()
mycursor_resume.execute("TRUNCATE TABLE resume")
mycursor_resume.execute("ALTER TABLE resume AUTO_INCREMENT = 1")
mydb_resume.commit()
def parse_resumes(text, items=50):
    mycursor_resume.execute("TRUNCATE TABLE resume")
    mycursor_resume.execute("ALTER TABLE resume AUTO_INCREMENT = 1")
    mydb_resume.commit()
    resume_count = 0
    page = 0
    while resume_count < items:
        url = f'https://hh.ru/search/resume?text={text}&exp_period=all_time&logic=normal&pos=full_text&page={page}'
        response = requests.get(url, headers=headers)
        soup = bs(response.text, 'lxml')
        data = soup.find_all('div', {'class': 'wrapper--eiknuhp1KcZ2hosUJO7g'})
        for i in data:
            try:
                position = i.find('a', 'bloko-link').text
                experience = i.find('div', {'class': 'content--uYCSpLiTsRfIZJe2wiYy'}).text.replace(' ', ' ')
                salary_str = i.find('div', {'class': 'bloko-text bloko-text_strong'}).text
                currency = salary_str[-2:]
                salary = salary_str[:-2].replace(' ', '')
                last_job = i.find('span', {'class': 'bloko-text bloko-text_strong'}).text
                mycursor_resume.execute("INSERT INTO resume (position, experience, salary, currency, last_job) VALUES (%s, %s, %s, %s, %s)",
                                 (position, experience, int(salary), currency, last_job))
                mydb_resume.commit()
                resume_count += 1
                if resume_count >= items:
                    break
            except:
                pass
        page += 1

def parse_vacancies(text, items=30):
    mycursor_vacancy.execute("TRUNCATE TABLE hh_vacancies2")
    mycursor_vacancy.execute("ALTER TABLE hh_vacancies2 AUTO_INCREMENT = 1")
    mydb_vacancy.commit()
    def get_url(page):
        try:
            url = f'https://hh.ru/search/vacancy?text={text}&salary=&ored_clusters=true&page={page}'
            response = requests.get(url, headers=headers)
            soup = bs(response.text, 'lxml')
            data = soup.find_all('div', {'class': 'vacancy-search-item__card'})
            for i in data:
                card_url = i.find('a').get('href')
                yield card_url
        except:
            pass


    def array():
        vacancy_count = 0
        page = 0
        while vacancy_count < items:
            try:
                for card_url in get_url(page):
                    response = requests.get(card_url, headers=headers)
                    soup = bs(response.text, 'lxml')
                    data = soup.find('div', {'class': 'wrapper-flat--H4DVL_qLjKLCo1sytcNI'})
                    data1 = soup.find('div', {'class': 'vacancy-company-redesigned'})
                    if data:
                        position = data.find('h1', {'class': 'bloko-header-section-1'}).text
                        salary = data.find('span', {
                            'class': 'magritte-text___pbpft_3-0-9 magritte-text_style-primary___AQ7MW_3-0-9 magritte-text_typography-label-1-regular___pi3R-_3-0-9'}).text.replace(
                            ' ', ' ')
                        description = data.find_all('p', {'class': 'vacancy-description-list-item'})
                        experience = description[0].text if description else "Не указано"
                        schedule1 = description[1].text
                        parts = schedule1.split(', ')
                        schedule = parts[0]
                        employment = parts[1] if len(parts) > 1 else None
                        company = data1.find('span',
                                             {'class': 'bloko-header-section-2 bloko-header-section-2_lite'}).text
                        address_element = data1.find('div', {
                            'class': 'magritte-text___pbpft_3-0-9 magritte-text_style-primary___AQ7MW_3-0-9 magritte-text_typography-paragraph-2-regular___VO638_3-0-9'})
                        address = address_element.find('p').text if address_element else None
                        if address is None:
                            address1_element = data1.find('span', {'class': 'magritte-text___tkzIl_4-1-4'})
                            address = address1_element.find('span').text if address1_element else None
                        yield position, company, experience.replace('Требуемый опыт работы: ',
                                                                    ''), salary, schedule, employment, address
                        # print(position, company, experience.replace('Требуемый опыт работы:', ''), salary, schedule, employment,  address)
                        vacancy_count += 1
                        if vacancy_count >= items:
                            break
                    page += 1
            except:
                pass

    for item in array():
        position, company, experience, salary, employment, schedule, address = item
        mycursor_vacancy.execute(
            "INSERT INTO hh_vacancies2 (position, company, experience, salary, employment, schedule, address) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (position, company, experience, salary, employment, schedule, address))
    mydb_vacancy.commit()

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')
@app.route('/process', methods=['POST'])
def process():
    text = request.form['text']
    parse_resumes(text)
    return redirect(url_for('index', text=text))
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    text = request.args.get('text', '')
    if request.method == 'POST':
        text = request.form.get('text')
        parse_resumes(text)
    mycursor_resume.execute("SELECT * FROM resume")
    resumes = mycursor_resume.fetchall()
    return render_template('index.html', resumes=resumes, text=text)


@app.route('/vacancies', methods=['GET', 'POST'])
def vacancies():
    if request.method == 'POST':
        text = request.form.get('text')
        employment_filter = request.form.getlist('employment')
        schedule_filter = request.form.getlist('schedule')
        experience_filter = request.form.getlist('experience')
        parse_vacancies(text)

        query = "SELECT * FROM hh_vacancies2"
        query_params = []
        filters = []
        if employment_filter:
            filters.append("employment IN ({})".format(', '.join(['%s'] * len(employment_filter))))
            query_params.extend(employment_filter)
        if schedule_filter:
            filters.append("schedule IN ({})".format(', '.join(['%s'] * len(schedule_filter))))
            query_params.extend(schedule_filter)
        if experience_filter:
            filters.append("experience IN ({})".format(', '.join(['%s'] * len(experience_filter))))
            query_params.extend(experience_filter)

        if filters:
            query += " WHERE " + " AND ".join(filters)

        mycursor_vacancy.execute(query, query_params)
        vacancies = mycursor_vacancy.fetchall()
        query_params.clear()
        filters.clear()
        return render_template('vacancies.html', vacancies=vacancies, text=text)
    else:
        mycursor_vacancy.execute("SELECT * FROM hh_vacancies2")
        vacancies = mycursor_vacancy.fetchall()
        return render_template('vacancies.html', vacancies=vacancies)


if __name__ == '__main__':
    app.run(debug=True)

