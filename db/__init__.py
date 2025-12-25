from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import re

db = SQLAlchemy()

# Модель пользователя
class users(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20), unique=True)
    account_number = db.Column(db.String(20), unique=True, default='')
    balance = db.Column(db.Float, default=1000.0)
    is_manager = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<User {self.login}>'
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

# Модель транзакций
class transactions(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    sender = db.relationship('users', foreign_keys=[from_user_id], backref='sent_transactions')
    receiver = db.relationship('users', foreign_keys=[to_user_id], backref='received_transactions')

# Функции валидации
def validate_login(login):
    return bool(re.match(r'^[a-zA-Z0-9._-]+$', login) and 3 <= len(login) <= 30)

def validate_password(password):
    return bool(re.match(r'^[a-zA-Z0-9!@#$%^&*._-]+$', password) and len(password) >= 6)

def validate_phone(phone):
    return bool(re.match(r'^\+?[1-9]\d{1,14}$', phone))

def validate_amount(amount):
    return amount > 0

# Инициализация БД
def init_db(app):
    with app.app_context():
        db.create_all()
        
        # Создаем тестовых пользователей, если их нет
        if users.query.count() == 0:
            print("Создание тестовых пользователей...")
            
            # 10 клиентов
            clients = [
                ("Иванов Иван Иванович", "client1", "123456", "+79991234567"),
                ("Петров Петр Петрович", "client2", "123456", "+79991234568"),
                ("Сидорова Анна Сергеевна", "client3", "123456", "+79991234569"),
                ("Козлов Дмитрий Алексеевич", "client4", "123456", "+79991234570"),
                ("Морозова Екатерина Владимировна", "client5", "123456", "+79991234571"),
                ("Васильев Сергей Михайлович", "client6", "123456", "+79991234572"),
                ("Новикова Ольга Петровна", "client7", "123456", "+79991234573"),
                ("Смирнов Алексей Иванович", "client8", "123456", "+79991234574"),
                ("Федорова Мария Александровна", "client9", "123456", "+79991234575"),
                ("Кузнецов Павел Николаевич", "client10", "123456", "+79991234576"),
            ]
            
            for full_name, login, pwd, phone in clients:
                acc_num = str(uuid.uuid4())[:8].upper()
                user = users(
                    full_name=full_name,
                    login=login,
                    password=generate_password_hash(pwd),
                    phone=phone,
                    account_number=acc_num,
                    balance=1000.0
                )
                db.session.add(user)

            # 2 менеджера
            admin = users(
                full_name="Администратор банка",
                login="admin",
                password=generate_password_hash("admin123"),
                account_number="ADMIN001",
                is_manager=True,
                balance=100000.0
            )
            
            manager = users(
                full_name="Менеджер банка",
                login="manager",
                password=generate_password_hash("manager123"),
                account_number="MANAGER01",
                is_manager=True,
                balance=50000.0
            )
            
            db.session.add(admin)
            db.session.add(manager)
            db.session.commit()
            
            print(f"✅ Создано {users.query.count()} пользователей")