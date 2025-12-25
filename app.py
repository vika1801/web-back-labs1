from flask import Flask, url_for, request, redirect, make_response, render_template, abort, session, jsonify
import datetime
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from db import db, init_db, users
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# ========== 1. СОЗДАЕМ ПРИЛОЖЕНИЕ ==========
app = Flask(__name__)

# ========== 2. НАСТРАИВАЕМ КОНФИГУРАЦИЮ ==========
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

# Конфигурация
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cекретно-секретный-ключ-для-банка')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Настройка БД
if app.config['DB_TYPE'] == 'postgres':
    db_name = 'vika_sopova_orm'
    db_user = 'vika_sopova_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else: 
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "vika_sopova_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

# ========== 3. ИНИЦИАЛИЗИРУЕМ БД ==========
db.init_app(app)
with app.app_context():
    init_db(app)

# ========== 4. ИМПОРТИРУЕМ ТОЛЬКО НУЖНЫЕ ЛАБОРАТОРНЫЕ ==========
# Импорт ТОЛЬКО lab5 и lab9
from lab5 import lab5
from lab9 import lab9

# Импорт банковского модуля
from bank import bank

# Регистрация ТОЛЬКО lab5 и lab9
app.register_blueprint(lab5)
app.register_blueprint(lab9)

# Регистрация банковского модуля с префиксом
app.register_blueprint(bank, url_prefix='/bank')

# ========== 5. МАРШРУТЫ ПРИЛОЖЕНИЯ ==========
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
                <style>
                    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                    body {{ 
                        font-family: 'Arial', sans-serif; 
                        line-height: 1.6; 
                        color: #333;
                        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                        min-height: 100vh;
                    }}
                    .container {{ 
                        max-width: 1200px; 
                        margin: 0 auto; 
                        padding: 20px; 
                    }}
                    header {{ 
                        background: #1e3c72; 
                        color: white; 
                        padding: 2rem 0;
                        text-align: center;
                        margin-bottom: 2rem;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }}
                    header h1 {{ 
                        font-size: 2.5rem; 
                        margin-bottom: 1rem;
                    }}
                    nav {{ 
                        background: white; 
                        border-radius: 10px;
                        padding: 2rem;
                        margin-bottom: 2rem;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    }}
                    nav ul {{ 
                        list-style: none;
                        display: grid;
                        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                        gap: 1rem;
                    }}
                    nav li {{ 
                        margin-bottom: 0.5rem;
                    }}
                    nav a {{ 
                        display: block;
                        padding: 1rem;
                        background: #f8f9fa;
                        border-radius: 8px;
                        text-decoration: none;
                        color: #1e3c72;
                        font-weight: 500;
                        transition: all 0.3s ease;
                        border: 2px solid transparent;
                    }}
                    nav a:hover {{ 
                        background: #1e3c72;
                        color: white;
                        transform: translateY(-2px);
                        box-shadow: 0 6px 12px rgba(30, 60, 114, 0.2);
                        border-color: #1e3c72;
                    }}
                    .main-content {{ 
                        background: white; 
                        padding: 2rem;
                        border-radius: 10px;
                        margin-bottom: 2rem;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    }}
                    .main-content h2 {{ 
                        color: #1e3c72;
                        margin-bottom: 1rem;
                        border-bottom: 3px solid #1e3c72;
                        padding-bottom: 0.5rem;
                    }}
                    footer {{ 
                        background: #1e3c72; 
                        color: white; 
                        padding: 2rem 0;
                        text-align: center;
                        margin-top: 2rem;
                        border-radius: 10px 10px 0 0;
                    }}
                    .footer-content {{ 
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                        gap: 2rem;
                        text-align: left;
                    }}
                    .footer-section h3 {{ 
                        margin-bottom: 1rem;
                        font-size: 1.2rem;
                    }}
                    .highlight {{ 
                        background: linear-gradient(135deg, #4CAF50, #2E7D32);
                        color: white;
                        padding: 1rem;
                        border-radius: 8px;
                        font-weight: bold;
                        margin: 1rem 0;
                        text-align: center;
                    }}
                    @media (max-width: 768px) {{
                        nav ul {{ grid-template-columns: 1fr; }}
                        .footer-content {{ grid-template-columns: 1fr; }}
                    }}
                </style>
            </head>
            <body>
                <header>
                    <div class="container">
                        <h1>WEB-программирование, часть 2</h1>
                        <p>ФБИ-31 | Сопова Виктория Андреевна</p>
                    </div>
                </header>
                
                <div class="container">
                    <nav>
                        <h2 style="color: #1e3c72; margin-bottom: 1.5rem; text-align: center;">📚 Доступные лабораторные работы</h2>
                        <ul>
                            <li><a href="/lab5">🔬 Лабораторная работа 5</a></li>
                            <li><a href="/lab9">🔬 Лабораторная работа 9</a></li>
                            <li><a href="/bank" style="background: linear-gradient(135deg, #4CAF50, #2E7D32); color: white;">🏦 РГЗ - Банковская система</a></li>
                        </ul>
                    </nav>
                    
                    <div class="main-content">
                        <h2>🚀 О проекте</h2>
                        <p>Данный проект представляет собой сборник лабораторных работ по дисциплине "WEB-программирование, часть 2".</p>
                        
                        <div class="highlight">
                            🎯 <strong>РГЗ - Банковская система</strong> - полнофункциональное веб-приложение с авторизацией, 
                            переводами между пользователями и админ-панелью.
                        </div>
                        
                        <h3>📋 Основные возможности банковской системы:</h3>
                        <ul style="margin-left: 2rem; margin-top: 1rem;">
                            <li>🔐 Два типа пользователей: клиенты и менеджеры</li>
                            <li>💳 Переводы денег между пользователями</li>
                            <li>📊 Просмотр истории операций</li>
                            <li>👥 Управление пользователями (для менеджеров)</li>
                            <li>✅ Валидация всех входных данных</li>
                            <li>🔒 Безопасное хранение паролей</li>
                        </ul>
                        
                        <h3 style="margin-top: 2rem;">🧪 Тестовые данные для входа:</h3>
                        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                            <p><strong>👨‍💼 Менеджер:</strong> логин: <code>admin</code>, пароль: <code>admin123</code></p>
                            <p><strong>👤 Клиент:</strong> логин: <code>client1</code>, пароль: <code>123456</code></p>
                            <p><small>Всего создано 10 клиентов (client1...client10) и 2 менеджера</small></p>
                        </div>
                    </div>
                </div>
                
                <footer>
                    <div class="container">
                        <div class="footer-content">
                            <div class="footer-section">
                                <h3>👨‍🎓 Студент</h3>
                                <p><strong>ФИО:</strong> Сопова Виктория Андреевна</p>
                                <p><strong>Группа:</strong> ФБИ-31</p>
                                <p><strong>Курс:</strong> 3</p>
                            </div>
                            
                            <div class="footer-section">
                                <h3>📅 Год выполнения</h3>
                                <p>2025 год</p>
                                <p>Веб-программирование, часть 2</p>
                            </div>
                            
                            <div class="footer-section">
                                <h3>🔗 Быстрые ссылки</h3>
                                <p><a href="/bank" style="color: #4CAF50;">🏦 Перейти в банковскую систему</a></p>
                                <p><a href="/lab5" style="color: white;">🔬 Лабораторная работа 5</a></p>
                                <p><a href="/lab9" style="color: white;">🔬 Лабораторная работа 9</a></p>
                            </div>
                        </div>
                        
                        <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1);">
                            <p>© 2025 | Все лабораторные работы выполнены в рамках учебного курса</p>
                        </div>
                    </div>
                </footer>
            </body>
        </html>
    """ 

# ========== РЕДИРЕКТ НА БАНК ==========
@app.route("/bank")
def bank_redirect():
    return redirect('/bank/')

# ========== РЕДИРЕКТЫ ДЛЯ НЕДОСТУПНЫХ ЛАБОРАТОРНЫХ ==========
@app.route("/lab1")
@app.route("/lab2")
@app.route("/lab3")
@app.route("/lab4")
@app.route("/lab6")
@app.route("/lab7")
@app.route("/lab8")
def lab_redirect():
    return redirect('/')

# ========== ОБРАБОТЧИКИ ОШИБОК ==========
@app.errorhandler(404)
def not_found(err):
    return """
        <!doctype html>
        <html>
            <head>
                <title>404 - Страница не найдена</title>
                <style>
                    body { font-family: Arial; text-align: center; padding: 50px; }
                    h1 { color: #d9534f; }
                    .info { margin: 20px 0; }
                </style>
            </head>
            <body>
                <h1>404 - Страница не найдена</h1>
                <div class="info">К сожалению, запрашиваемая страница не существует.</div>
                <a href="/">Вернуться на главную</a><br>
                <a href="/bank">Перейти в банковскую систему</a>
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
                        font-family: Arial; 
                        text-align: center; 
                        padding: 50px; 
                        background: #f8d7da;
                    }
                    h1 { color: #721c24; }
                    .error-container { 
                        background: white; 
                        padding: 30px; 
                        border-radius: 10px;
                        max-width: 600px;
                        margin: 0 auto;
                    }
                </style>
            </head>
            <body>
                <div class="error-container">
                    <h1>500 - Внутренняя ошибка сервера</h1>
                    <p>На сервере произошла непредвиденная ошибка.</p>
                    <p>Мы уже работаем над устранением проблемы.</p>
                    <a href="/">Вернуться на главную</a><br>
                    <a href="/bank">Перейти в банковскую систему</a>
                </div>
            </body>
        </html>
        """, 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)