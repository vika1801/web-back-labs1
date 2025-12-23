from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab8 = Blueprint('lab8', __name__)  

@lab8.route('/lab8/')
def main():
    return render_template('lab8/index.html')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    if not (login or password):
        return render_template('lab8/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?", (login,))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return render_template('lab8/login.html', error = 'Логин и/или пароль неверны')
    if not check_password_hash (user['password'], password):
        db_close(conn, cur) 
        return render_template ('lab8/login.html', error='Логин и/или пароль неверны')
    session['login'] = login
    db_close(conn, cur) 
    return render_template('lab8/success_login.html', login=login)


@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab8/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;",(login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;",(login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab8/register.html', error= 'Такой пользователь уже существует')

    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))

    db_close(conn, cur)
    return render_template('lab8/success.html', login=login)

@lab8.route('/lab8/articles')
def articles():
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT articles.id, articles.title, articles.article_text, 
                   articles.created_at, users.login as author
            FROM articles 
            JOIN users ON articles.user_id = users.id 
            ORDER BY articles.created_at DESC
        """)
    else:
        cur.execute("""
            SELECT articles.id, articles.title, articles.article_text, 
                   articles.created_at, users.login as author
            FROM articles 
            JOIN users ON articles.user_id = users.id 
            ORDER BY articles.created_at DESC
        """)
    
    articles_list = cur.fetchall()
    current_user = session.get('login', 'anonymous')
    
    db_close(conn, cur)
    
    return render_template('lab8/articles.html', 
                          articles=articles_list, 
                          current_user=current_user)

@lab8.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return render_template('lab8/login.html')
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    if not title or not article_text:  
            return render_template('lab8/create_article.html', error='Все поля должны быть заполнены!')
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute('SELECT id FROM users WHERE login=%s;', (login, ))
    else:
        cur.execute('SELECT id FROM users WHERE login=?;', (login, ))
    user_id = cur.fetchone()['id']
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);", (user_id, title, article_text))
    else:
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (?, ?, ?);", (user_id, title, article_text))
    db_close(conn, cur)
    return redirect ('/lab8')

