from flask import Blueprint, render_template, request, session
import psycopg2

lab6 = Blueprint('lab6', __name__)

def get_db_connection():
    """Создание подключения к базе данных"""
    conn = psycopg2.connect(
        host="localhost",
        database="vika_sopova_knowledge_base",
        user="vika_sopova_knowledge_base",
        password="123",
        port=5432
    )
    return conn

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']

    if data['method'] == 'info':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT number, tenant, price FROM offices ORDER BY number')
        offices_data = cur.fetchall()
        cur.close()
        conn.close()
        
        # Преобразуем в формат JSON
        offices = []
        for office in offices_data:
            offices.append({
                'number': office[0],
                'tenant': office[1] if office[1] else '',
                'price': office[2]
            })
        
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Проверяем, свободен ли офис
        cur.execute('SELECT tenant FROM offices WHERE number = %s', (office_number,))
        office = cur.fetchone()
        
        if not office:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'Office not found'
                },
                'id': id
            }
        
        if office[0]:  # Если tenant не пустой
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }
        
        # Бронируем офис
        cur.execute('UPDATE offices SET tenant = %s WHERE number = %s', (login, office_number))
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id 
        }
    
    if data['method'] == 'cancellation':
        office_number = data['params']
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Получаем информацию об офисе
        cur.execute('SELECT tenant FROM offices WHERE number = %s', (office_number,))
        office = cur.fetchone()
        
        if not office:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'Office not found'
                },
                'id': id
            }
        
        if not office[0]:  # Если офис не арендован
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office is not rented'
                },
                'id': id
            }
        
        if office[0] != login:  # Если офис арендован другим пользователем
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'Вы можете отменить только свою аренду'
                },
                'id': id
            }
        
        # Снимаем аренду
        cur.execute('UPDATE offices SET tenant = %s WHERE number = %s', ('', office_number))
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }
        
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }