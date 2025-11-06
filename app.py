from flask import Flask, url_for, request, redirect, make_response, render_template, abort
import datetime

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4

app = Flask(__name__)
app.register_blueprint(lab1) 
app.register_blueprint(lab2) 
app.register_blueprint(lab3) 
app.register_blueprint(lab4) 


@app.route("/")
@app.route('/index')
def start():
    css_url = url_for('static', filename='lab1/main.css')
    favicon_ico_url = url_for('static', filename='lab2/favicon.ico')
    favicon_32_url = url_for('static', filename='lab2/favicon-32x32.png')
    favicon_16_url = url_for('static', filename='lab2/favicon-16x16.png')
    return f"""
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="{css_url}">
                <link rel="icon" href="{favicon_ico_url}" type="image/x-icon">
                <link rel="icon" href="{favicon_32_url}">
                <link rel="icon" href="{favicon_16_url}">
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
                    <ul>
                        <li><a href="/lab2">Вторая лабораторная</a></li>
                    </ul>
                    <ul>
                        <li><a href="/lab3">Третья лабораторная</a></li>
                    </ul>
                    <ul>
                        <li><a href="/lab4">Четвертая лабораторная</a></li>
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
        </html>
        """


@app.errorhandler(404)
def not_found(err):
    css_url = url_for('static', filename='lab1/lab1.css')
    image_url = url_for('static', filename='lab1/error.jpg')
    
    return f"""
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
        """, 404


@app.errorhandler(500)
def internal_server_error(error):
    return """
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
        """, 500

