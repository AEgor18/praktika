from flask import Flask, render_template, request, url_for
import mysql.connector

app = Flask(__name__)

# Настройки базы данных
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='(Promo456)',
    database='hh_resume'
)

mycursor = mydb.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        mycursor.execute("SELECT * FROM resume WHERE position LIKE %s", ('%' + text + '%',))
        resumes = mycursor.fetchall()
    else:
        mycursor.execute("SELECT * FROM resume")
        resumes = mycursor.fetchall()
    return render_template('index.html', resumes=resumes)

if __name__ == '__main__':
    app.run(debug=True)