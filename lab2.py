from flask import Blueprint, redirect, url_for, render_template
lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a/')
def a():
    return 'ok'

flower_list = ('роза', 'тюльпан', 'незабудка', 'ромашка')

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок: " + flower_list[flower_id]
    

@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f"""
        <!doctype html>
        <html>
            <body>
            <h1>Добавлен новый цветок</h1>
            <p>Название нового цветка: {name} </p>
            <p>Всего цветов: {len(flower_list)}</p>
            <p>Полный список: {flower_list}</p>
            </body>
        </html>
        """


@lab2.route('/lab2/example/')
def example():
    name, lab_num, group, course = 'Вика Сопова', 2, 'ФБИ-31', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/example.html',
                           name=name, lab_num=lab_num, group=group,
                           course=course, fruits=fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase = phrase)


@lab2.route('/lab2/add_flower/')
def add_flower_empty():
    return "Вы не задали имя цветка", 400


@lab2.route('/lab2/flowers/')
def all_flowers():
    return render_template('lab2/flowers.html', flowers=flower_list)


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers2(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    return render_template('lab2/flower_id.html', flower_id=flower_id, flower=flower_list[flower_id])


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers/')


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('lab2/calc.html', a=a, b=b)


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')




