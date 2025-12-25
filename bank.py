from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from db import db, users, transactions, validate_login, validate_password, validate_phone, validate_amount
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime
from functools import wraps

bank = Blueprint('bank', __name__, template_folder='templates/rgz')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Требуется авторизация'}), 401
        return f(*args, **kwargs)
    return decorated_function

def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Требуется авторизация'}), 401
        
        user = users.query.get(session['user_id'])
        if not user or not user.is_manager:
            return jsonify({'error': 'Доступ запрещен. Требуются права менеджера.'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@bank.route('/')
def index():
    return redirect(url_for('bank.login_page'))

@bank.route('/login', methods=['GET'])
def login_page():
    if 'user_id' in session:
        return redirect(url_for('bank.dashboard'))
    return render_template('login.html')

@bank.route('/login', methods=['POST'])
def login_api():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных'}), 400
        
        login_input = data.get('login', '').strip()
        password = data.get('password', '').strip()
        
        if not validate_login(login_input):
            return jsonify({'error': 'Неверный формат логина'}), 400
        
        user = users.query.filter_by(login=login_input).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['login'] = user.login
            session['full_name'] = user.full_name
            session['account_number'] = user.account_number
            session['is_manager'] = user.is_manager
            
            return jsonify({
                'success': True,
                'redirect': url_for('bank.dashboard'),
                'user': {
                    'id': user.id,
                    'login': user.login,
                    'full_name': user.full_name,
                    'is_manager': user.is_manager
                }
            })
        
        return jsonify({'error': 'Неверный логин или пароль'}), 401
        
    except Exception as e:
        return jsonify({'error': f'Ошибка сервера: {str(e)}'}), 500

@bank.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('bank.login_page'))

@bank.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('bank.login_page'))
    
    user = users.query.get(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('bank.login_page'))
    
    if user.is_manager:
        return render_template('manager_dashboard.html', user=user)
    else:
        return render_template('client_dashboard.html', user=user)

@bank.route('/api/transfer', methods=['POST'])
@login_required
def api_transfer():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных'}), 400
        
        amount = float(data.get('amount', 0))
        recipient = data.get('recipient', '').strip()
        
        if not validate_amount(amount):
            return jsonify({'error': 'Сумма должна быть больше 0'}), 400
        
        user = users.query.get(session['user_id'])
        
        if user.balance < amount:
            return jsonify({'error': 'Недостаточно средств'}), 400
        
        recipient_user = None
        if recipient.startswith('+'):
            recipient_user = users.query.filter_by(phone=recipient).first()
        else:
            recipient_user = users.query.filter_by(account_number=recipient).first()
        
        if not recipient_user:
            return jsonify({'error': 'Получатель не найден'}), 404
        
        if recipient_user.id == user.id:
            return jsonify({'error': 'Нельзя перевести самому себе'}), 400
        
        user.balance -= amount
        recipient_user.balance += amount
        
        transaction = transactions(
            from_user_id=user.id,
            to_user_id=recipient_user.id,
            amount=amount
        )
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'new_balance': user.balance,
            'message': f'Перевод {amount:.2f}₽ успешно выполнен'
        })
        
    except ValueError:
        return jsonify({'error': 'Неверный формат суммы'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Ошибка перевода: {str(e)}'}), 500

@bank.route('/api/history')
@login_required
def api_history():
    try:
        user = users.query.get(session['user_id'])
        
        sent = transactions.query.filter_by(from_user_id=user.id).all()
        received = transactions.query.filter_by(to_user_id=user.id).all()
        
        history = []
        
        for t in sent:
            receiver = users.query.get(t.to_user_id)
            history.append({
                'id': t.id,
                'from_user': user.login,
                'to_user': receiver.login if receiver else 'Неизвестно',
                'amount': float(t.amount),
                'date': t.created_at.isoformat(),
                'type': 'outgoing'
            })
        
        for t in received:
            sender = users.query.get(t.from_user_id)
            history.append({
                'id': t.id,
                'from_user': sender.login if sender else 'Неизвестно',
                'to_user': user.login,
                'amount': float(t.amount),
                'date': t.created_at.isoformat(),
                'type': 'incoming'
            })
        
        history.sort(key=lambda x: x['date'], reverse=True)
        
        return jsonify(history[:50])
        
    except Exception as e:
        return jsonify({'error': f'Ошибка загрузки истории: {str(e)}'}), 500

@bank.route('/api/users', methods=['GET'])
@manager_required
def get_users():
    try:
        all_users = users.query.order_by(users.is_manager.desc(), users.full_name).all()
        
        users_list = []
        for u in all_users:
            users_list.append({
                'id': u.id,
                'full_name': u.full_name,
                'login': u.login,
                'phone': u.phone or '',
                'account_number': u.account_number,
                'balance': float(u.balance),
                'is_manager': u.is_manager
            })
        
        return jsonify(users_list)
        
    except Exception as e:
        return jsonify({'error': f'Ошибка загрузки пользователей: {str(e)}'}), 500

@bank.route('/api/users', methods=['POST'])
@manager_required
def create_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных'}), 400
        
        full_name = data.get('full_name', '').strip()
        login_input = data.get('login', '').strip()
        password = data.get('password', '').strip()
        phone = data.get('phone', '').strip()
        is_manager = data.get('is_manager', False)
        
        if not all([full_name, login_input, password]):
            return jsonify({'error': 'Заполните все обязательные поля'}), 400
        
        if not validate_login(login_input):
            return jsonify({'error': 'Неверный формат логина'}), 400
        
        if not validate_password(password):
            return jsonify({'error': 'Пароль должен содержать минимум 6 символов'}), 400
        
        if phone and not validate_phone(phone):
            return jsonify({'error': 'Неверный формат телефона'}), 400
        
        if users.query.filter_by(login=login_input).first():
            return jsonify({'error': 'Логин уже существует'}), 400
        
        if phone and users.query.filter_by(phone=phone).first():
            return jsonify({'error': 'Телефон уже используется'}), 400
        
        account_number = str(uuid.uuid4())[:8].upper()
        while users.query.filter_by(account_number=account_number).first():
            account_number = str(uuid.uuid4())[:8].upper()
        
        new_user = users(
            full_name=full_name,
            login=login_input,
            password=generate_password_hash(password),
            phone=phone if phone else None,
            account_number=account_number,
            is_manager=bool(is_manager),
            balance=1000.0 if not is_manager else 50000.0
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Пользователь {full_name} успешно создан',
            'account_number': account_number
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Ошибка создания пользователя: {str(e)}'}), 500

@bank.route('/api/users', methods=['DELETE'])
@manager_required
def delete_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных'}), 400
        
        user_id = data.get('id')
        
        if user_id == session['user_id']:
            return jsonify({'error': 'Нельзя удалить свой аккаунт'}), 400
        
        user_to_delete = users.query.get(user_id)
        if not user_to_delete:
            return jsonify({'error': 'Пользователь не найден'}), 404
        
        db.session.delete(user_to_delete)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Пользователь {user_to_delete.login} удален'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Ошибка удаления пользователя: {str(e)}'}), 500
