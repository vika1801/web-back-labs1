from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for

lab9 = Blueprint('lab9', __name__)

opened_boxes = set()

boxes = [
    {'id': 0, 'text': 'С Новым годом! Пусть этот год принесёт вам счастье и радость!', 'img': 'lab9/images/gift1.jpg'},
    {'id': 1, 'text': 'Желаю вам крепкого здоровья и благополучия в наступающем году!', 'img': 'lab9/images/gift2.jpg'},
    {'id': 2, 'text': 'Пусть Новый год подарит вам море позитива и улыбок!', 'img': 'lab9/images/gift3.jpg'},
    {'id': 3, 'text': 'С наступающим! Пусть все мечты сбываются!', 'img': 'lab9/images/gift4.jpg'},
    {'id': 4, 'text': 'Желаю вам успехов во всех начинаниях и достижения целей!', 'img': 'lab9/images/gift5.jpg'},
    {'id': 5, 'text': 'Пусть Новый год принесёт вам удачу и процветание!', 'img': 'lab9/images/gift6.jpg', 'auth': True},
    {'id': 6, 'text': 'С Новым годом! Пусть в вашей жизни будет много радостных моментов!', 'img': 'lab9/images/gift7.jpg'},
    {'id': 7, 'text': 'Желаю вам тепла, уюта и семейного счастья!', 'img': 'lab9/images/gift8.jpg', 'auth': True},
    {'id': 8, 'text': 'Пусть Новый год откроет перед вами новые возможности!', 'img': 'lab9/images/gift9.jpg'},
    {'id': 9, 'text': 'С наступающим Новым годом! Пусть сбудутся все ваши желания!', 'img': 'lab9/images/gift10.jpg', 'auth': True},
]

positions = [
    {'top': 10, 'left': 8},   # 0
    {'top': 10, 'left': 22},  # 1  
    {'top': 10, 'left': 36},  # 2
    {'top': 10, 'left': 50},  # 3
    {'top': 10, 'left': 64},  # 4
    
    {'top': 35, 'left': 8},   # 5
    {'top': 35, 'left': 22},  # 6
    {'top': 35, 'left': 36},  # 7
    {'top': 35, 'left': 50},  # 8
    {'top': 35, 'left': 64},  # 9
]


@lab9.route('/lab9/')
def lab():
    if 'opened_count' not in session:
        session['opened_count'] = 0
    
    unopened = len(boxes) - len(opened_boxes)
    
    # ЖЁСТКАЯ проверка — ТОЛЬКО известные ключи из lab5
    authorized_keys = ['login', 'username', 'user_id', 'user_name']
    is_authorized = any(session.get(key) for key in authorized_keys)
    login = "👤 Авторизованный пользователь" if is_authorized else None
    
    return render_template('lab9/index.html', unopened=unopened, login=login)

@lab9.route('/lab9/rest-api/boxes', methods=['GET'])
def get_boxes():
    authorized_keys = ['login', 'username', 'user_id', 'user_name']
    is_authorized = any(session.get(key) for key in authorized_keys)
    
    result = []
    for i in range(len(boxes)):
        box = boxes[i]
        result.append({
            'id': box['id'],
            'top': positions[i]['top'],
            'left': positions[i]['left'],
            'opened': box['id'] in opened_boxes,
            'need_auth': box.get('auth', False) and not is_authorized,
            'img': url_for('static', filename=box['img'])
        })
    return jsonify(result)

@lab9.route('/lab9/rest-api/open/<int:box_id>', methods=['POST'])
def open_box(box_id):
    if box_id < 0 or box_id >= len(boxes):
        return jsonify({'error': 'Коробка не найдена'}), 404
    
    if box_id in opened_boxes:
        return jsonify({'error': 'Эта коробка уже пуста!'}), 400
    
    if 'opened_count' not in session:
        session['opened_count'] = 0
    
    if session['opened_count'] >= 3:
        return jsonify({'error': 'Вы уже открыли 3 коробки! Больше открывать нельзя.'}), 400
    
    box = boxes[box_id]
    
    # ЖЁСТКАЯ проверка авторизации
    authorized_keys = ['login', 'username', 'user_id', 'user_name']
    is_authorized = any(session.get(key) for key in authorized_keys)
    
    if box.get('auth', False) and not is_authorized:
        return jsonify({'error': '🔒 Этот подарок только для авторизованных! Войдите через /lab5/login'}), 403
    
    opened_boxes.add(box_id)
    session['opened_count'] += 1
    
    unopened = len(boxes) - len(opened_boxes)
    
    return jsonify({
        'text': box['text'],
        'img': url_for('static', filename=box['img']),
        'unopened': unopened
    })

@lab9.route('/lab9/rest-api/reset', methods=['POST'])
def reset():
    authorized_keys = ['login', 'username', 'user_id', 'user_name']
    is_authorized = any(session.get(key) for key in authorized_keys)
    
    if not is_authorized:
        return jsonify({'error': '🔒 Только для авторизованных!'}), 403
    
    opened_boxes.clear()
    session['opened_count'] = 0
    return jsonify({'message': 'Дед Мороз наполнил все коробки подарками!'})

@lab9.route('/lab9/logout')
def logout():
    session.clear()
    return redirect('/lab9/')
