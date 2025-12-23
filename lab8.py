from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/index.html')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/login.html', error='Введите логин')
    
    if not password_form:
        return render_template('lab8/login.html', error='Введите пароль')

    user = users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=False)
        return redirect('/lab8/')
    
    return render_template('lab8/login.html', error='Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')
    
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()

    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/lab8/')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).order_by(articles.id.desc()).all()
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = 'is_favorite' in request.form
    is_public = 'is_public' in request.form
    
    if not title:
        return render_template('lab8/create_article.html', error='Введите заголовок статьи')
    
    if not article_text:
        return render_template('lab8/create_article.html', error='Введите текст статьи')
    
    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=is_favorite,
        is_public=is_public,
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/article/<int:article_id>')
def view_article(article_id):
    article = articles.query.get_or_404(article_id)
    author = users.query.get(article.login_id) if article.login_id else None
    return render_template('lab8/article.html', article=article, author=author)

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    if article.login_id != current_user.id:
        return redirect('/lab8/articles')
    
    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = 'is_favorite' in request.form
    is_public = 'is_public' in request.form
    
    if not title or not article_text:
        return render_template('lab8/edit_article.html', article=article, error='Заполните все поля')
    
    article.title = title
    article.article_text = article_text
    article.is_favorite = is_favorite
    article.is_public = is_public
    
    db.session.commit()
    return redirect(f'/lab8/article/{article_id}')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    if article.login_id != current_user.id:
        return redirect('/lab8/articles')
    
    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/like/<int:article_id>', methods=['POST'])
@login_required
def like_article(article_id):
    article = articles.query.get_or_404(article_id)
    article.likes = (article.likes or 0) + 1
    db.session.commit()
    return redirect(f'/lab8/article/{article_id}')
