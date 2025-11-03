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
    css_url = url_for('static', filename='lab1.css')
    image_url = url_for('static', filename='error.jpg')
    
    return f'''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <link rel="stylesheet" href="{css_url}">
        <style>
            .error-container {{
                text-align: center;
                padding: 50px;
            }}
            .error-image {{
                max-width: 400px;
                height: auto;
                margin: 20px 0;
            }}
            .error-message {{
                color: #d9534f;
                font-size: 24px;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1>404 - Страница не найдена</h1>
            <div class="error-message">нет такой страницы</div>
            <img src="{image_url}" alt="Ошибка 404" class="error-image">
            <br>
            <a href="/">Вернуться на главную</a>
            <br>
            <a href="/lab1">К лабораторной работе</a>
        </div>
    </body>
</html>
''', 404

@app.route('/lab1/counter/reset')
def reset_counter():
    global count
    count = 0
    return "Счётчик сброшен. <a href='/lab1/counter'>Вернуться к счётчику</a>"

@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <div class="container">
            <h1>Лабораторная работа 1</h1>
            
            <div class="description">
                <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, 
                использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. 
                Относится к категории так называемых микрофреймворков — минималистичных 
                каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
            </div>
            
            <a href="/" class="back-link">Вернуться на главную страницу</a>
        </div>
    </body>
</html>
'''

@app.route('/lab1/400')
def bad_request():
    return '''
<!doctype html>
<html>
    <head>
        <title>400 - Bad Request</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .error { color: #d9534f; background: #f8d7da; padding: 20px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="error">
            <h1>400 - Bad Request</h1>
            <p>Неверный запрос. Сервер не может обработать запрос из-за синтаксической ошибки.</p>
        </div>
        <a href="/">На главную</a> | 
        <a href="/lab1">К лабораторной</a>
    </body>
</html>
''', 400

@app.route('/lab1/401')
def unauthorized():
    return '''
<!doctype html>
<html>
    <head>
        <title>401 - Unauthorized</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .error { color: #856404; background: #fff3cd; padding: 20px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="error">
            <h1>401 - Unauthorized</h1>
            <p>Требуется аутентификация. Для доступа к ресурсу необходима авторизация.</p>
        </div>
        <a href="/">На главную</a> | 
        <a href="/lab1">К лабораторной</a>
    </body>
</html>
''', 401

@app.route('/lab1/402')
def payment_required():
    return '''
<!doctype html>
<html>
    <head>
        <title>402 - Payment Required</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .error { color: #0c5460; background: #d1ecf1; padding: 20px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="error">
            <h1>402 - Payment Required</h1>
            <p>Необходима оплата. Этот код был зарезервирован для использования в системах цифровых платежей.</p>
            <p>В настоящее время он редко используется, но был определён для будущего применения.</p>
        </div>
        <a href="/">На главную</a> | 
        <a href="/lab1">К лабораторной</a>
    </body>
</html>
''', 402

@app.route('/lab1/403')
def forbidden():
    return '''
<!doctype html>
<html>
    <head>
        <title>403 - Forbidden</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .error { color: #721c24; background: #f8d7da; padding: 20px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="error">
            <h1>403 - Forbidden</h1>
            <p>Доступ запрещен. У вас нет прав для доступа к этому ресурсу.</p>
        </div>
        <a href="/">На главную</a> | 
        <a href="/lab1">К лабораторной</a>
    </body>
</html>
''', 403

@app.route('/lab1/405')
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <head>
        <title>405 - Method Not Allowed</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .error { color: #155724; background: #d4edda; padding: 20px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="error">
            <h1>405 - Method Not Allowed</h1>
            <p>Метод не разрешен. Использованный метод HTTP не поддерживается для данного ресурса.</p>
        </div>
        <a href="/">На главную</a> | 
        <a href="/lab1">К лабораторной</a>
    </body>
</html>
''', 405

@app.route('/lab1/418')
def teapot():
    return '''
<!doctype html>
<html>
    <head>
        <title>418 - I'm a teapot</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
            .teapot { color: #8B4513; background: #FFF8DC; padding: 30px; border-radius: 10px; }
            .teapot-img { font-size: 50px; margin: 20px; }
        </style>
    </head>
    <body>
        <div class="teapot">
            <div class="teapot-img">🫖</div>
            <h1>418 - I'm a teapot</h1>
            <p>Я - чайник! Этот код был введен как апрельская шутка в 1998 году.</p>
            <p>Сервер отказывается варить кофе, потому что он - заварочный чайник.</p>
        </div>
        <a href="/">На главную</a> | 
        <a href="/lab1">К лабораторной</a>
    </body>
</html>
''', 418