from flask import Flask, url_for, request, redirect, make_response, render_template, abort
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
        <div class="header-info">
                <strong>Демонстрация HTTP-заголовков:</strong><br>
                • Content-Language: ru<br>
                • X-Student-Name: Sopova-Viktoria<br>
                • X-Lab-Work: 1
            </div>
            
            <img src="{path}" alt="Величественный дуб">
            <p>Эта страница возвращает кастомные HTTP-заголовки для лабораторной работы</p>
            
            <div>
                <a href="/"> На главную</a>
                <a href="/lab1"> К лабораторной</a>
                <a href="/lab1/author"> Об авторе</a>
            </div>
        </div>
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
        <div class="info-item">
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
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f8f9fa;
                line-height: 1.6;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                text-align: center;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            p {
                text-align: justify;
                margin-bottom: 20px;
                font-size: 16px;
            }
            .back-link {
                display: inline-block;
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
               margin-bottom: 30px;
                font-weight: bold;
            }
            .back-link:hover {
                background-color: #2980b9;
            }
            .routes-list {
                background-color: #f1f8ff;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }
            .routes-list ul {
                list-style-type: none;
                padding: 0;
            }
            .routes-list li {
                margin: 10px 0;
                padding: 8px;
                background: white;
                border-radius: 4px;
                border-left: 4px solid #3498db;
            }
            .routes-list a {
                color: #2c3e50;
                text-decoration: none;
                font-weight: bold;
            }
            .routes-list a:hover {
                color: #3498db;
                text-decoration: underline;
            }
        </style>
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
            <h2>Список роутов</h2>
            <div class="routes-list">
                <ul>
                    <li><a href="/">Главная страница</a> (/)</li>
                    <li><a href="/index">Главная страница</a> (/index)</li>
                    <li><a href="/lab1/web">Страница Web</a> (/lab1/web)</li>
                    <li><a href="/lab1/author">Информация об авторе</a> (/lab1/author)</li>
                    <li><a href="/lab1/image">Картинка дуба</a> (/lab1/image)</li>
                    <li><a href="/lab1/counter">Счётчик посещений</a> (/lab1/counter)</li>
                    <li><a href="/lab1/info">Тест перенаправления</a> (/lab1/info)</li>
                    <li><a href="/lab1/reset">Сброс счётчика</a> (/lab1/reset)</li>
                    <li><a href="/lab1/400">400 - Bad Request</a> (/lab1/400)</li>
                    <li><a href="/lab1/401">401 - Unauthorized</a> (/lab1/401)</li>
                    <li><a href="/lab1/402">402 - Payment Required</a> (/lab1/402)</li>
                    <li><a href="/lab1/403">403 - Forbidden</a> (/lab1/403)</li>
                    <li><a href="/lab1/405">405 - Method Not Allowed</a> (/lab1/405)</li>
                    <li><a href="/lab1/418">418 - I'm a teapot</a> (/lab1/418)</li>
                    <li><a href="/lab1/break-server">Тест ошибки 500</a> (/lab1/break-server)</li>
                </ul>
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

@app.errorhandler(500)
def internal_server_error(error):
    return '''
<!doctype html>
<html>
    <head>
        <title>500 - Ошибка сервера</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                text-align: center;
                background: rgba(255, 255, 255, 0.1);
                padding: 50px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                max-width: 600px;
            }
            .error-code {
                font-size: 120px;
                font-weight: bold;
                margin: 0;
                text-shadow: 3px 3px 0 rgba(0, 0, 0, 0.2);
            }
            .error-title {
                font-size: 36px;
                margin: 20px 0;
                color: #fff;
            }
            .error-message {
                font-size: 18px;
                margin: 20px 0;
                line-height: 1.6;
                color: #ffeaea;
            }
            .warning-icon {
                font-size: 80px;
                margin: 30px 0;
                display: block;
            }
            .btn {
                display: inline-block;
                background: white;
                color: #ff6b6b;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 50px;
                margin: 10px;
                font-weight: bold;
                transition: all 0.3s ease;
                border: 2px solid white;
            }
            .btn:hover {
                background: transparent;
                color: white;
                transform: translateY(-3px);
            }
            .technical-info {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                margin: 30px 0;
                text-align: left;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="warning-icon">⚠️</div>
            <h1 class="error-code">500</h1>
            <h2 class="error-title">Внутренняя ошибка сервера</h2>
            
            <div class="error-message">
                <p>На сервере произошла непредвиденная ошибка.</p>
                <p>Мы уже работаем над устранением проблемы. Пожалуйста, попробуйте позже.</p>
            </div>

            <div class="technical-info">
                <h3>Техническая информация:</h3>
                <p>• Произошла внутренняя ошибка приложения</p>
                <p>• Сервер не смог обработать запрос</p>
                <p>• Администратор уведомлен о проблеме</p>
            </div>

            <div>
                <a href="/" class="btn">🏠 На главную страницу</a>
                <a href="javascript:history.back()" class="btn">↩️ Вернуться назад</a>
            </div>

            <div style="margin-top: 30px; font-size: 14px; color: #ffd1d1;">
                <p>Приносим извинения за временные неудобства</p>
            </div>
        </div>
    </body>
</html>
''', 500

@app.route('/lab1/break-server')
def break_server():
    '''
    Обработчик, который намеренно вызывает ошибку 500
    Для проверки запускайте сервер без флага --debug
    '''
    result = 1 / 0
    return "Этот код никогда не выполнится"

@app.route('/lab2/a/')
def a():
    return 'ok'

flower_list = ('роза', 'тюльпан', 'незабудка', 'ромашка')

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок: " + flower_list[flower_id]
    
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/example/')
def example():
    return render_template('example.html')
