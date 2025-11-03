from flask import Flask, url_for, request, redirect, make_response, render_template
import datetime
app = Flask(__name__) 

@app.route("/")
@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <head>
                <title>HTTP, ФБ, Лабораторные работы</title>
            </head>
            <body>
                <header>
                    <h1>HTTP, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
                </header>
                <nav>
                    <ul>
                        <li><a href="/lab1">Первая лабораторная</a></li>
                    </ul>
                </nav>
               <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
               <footer>
                    <p>ФИО: Сопова Виктория Андреевна</p>
                    <p>Группа: ФБИ-31</p>
                    <p>Курс: 3</p>
                    <p>Год: 2025</p>
            </footer>
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author():
    name = "Сопова Виктория Андреевна"
    group = "ФБИ-31"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Группа: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route('/lab1/image')
def image():
    path = url_for("static", filename="oak.jpg")
    css_url = url_for('static', filename='lab1.css')
    return '''
<!doctype html>
<html>
    <head>
            <link rel="stylesheet" href="{css_url}">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    current_time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str (count) + '''
        <hr>
        Дата и время: ''' + str(current_time) + '''<br>
        Запрошенный адрес: ''' + str(url) + '''<br>
        Ваш IP-АДРЕС: ''' + str(client_ip) + '''<br>
        <a href="/lab1/counter/reset">Сбросить счётчик</a>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.route('/lab1/counter/reset')
def reset_counter():
    global count
    count = 0
    return "Счётчик сброшен. <a href='/lab1/counter'>Вернуться к счётчику</a>"