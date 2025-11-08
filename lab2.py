from flask import Blueprint, redirect, url_for, render_template, abort
lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a/')
def a():
    return 'ok'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']
    

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


books = [
      {'title': 'Властелин колец', 'author': 'Джон Р. Р. Толкин,', 'genre': 'роман-эпопея', 'pages': 900},
      {'title': 'Гордость и предубеждение', 'author': 'Джейн Остин', 'genre': 'роман' , 'pages': 430},
      {'title': 'Тёмные начала', 'author': 'Филип Пулман', 'genre': 'фантастическая трилогия', 'pages': 500},
      {'title': 'Автостопом по галактике', 'author': 'Дуглас Адамс', 'genre': 'юмористический научно-фантастический роман', 'pages': 400},
      {'title': 'Гарри Поттер и Кубок огня', 'author': 'Джоан Роулинг', 'genre': 'фэнтези', 'pages': 647},
      {'title': 'Убить пересмешника', 'author': 'Харпер Ли',  'genre': 'роман-бестселлер', 'pages': 280},
      {'title': 'Винни Пух', 'author': 'Алан Александр Милн', 'genre': 'детская повесть' , 'pages': 30},
      {'title': '1984', 'author': 'Джордж Оруэлл', 'genre': 'роман-антиутопия', 'pages': 330},
      {'title': 'Лев, колдунья и платяной шкаф', 'author': 'Клайв Стэйплз Льюис',  'genre': 'фэнтези', 'pages': 650},
      {'title': 'Джейн Эйр', 'author': 'Шарлотта Бронте',  'genre': 'роман', 'pages': 340}
]

@lab2.route('/lab2/books')
def book():
      return render_template('lab2/books.html', books=books)


berries_list = [
    {'name': 'Клубника', 'image': 'strawberry.jpg', 'description': 'Сладкая красная ягода, богатая витамином C'},
    {'name': 'Малина', 'image': 'raspberry.jpg', 'description': 'Ароматная ягода с нежным вкусом, содержит антиоксиданты'},
    {'name': 'Черника', 'image': 'blueberry.jpg', 'description': 'Маленькая синяя ягода, полезна для зрения'},
    {'name': 'Ежевика', 'image': 'blackberry.webp', 'description': 'Тёмная ягода с кисло-сладким вкусом'},
    {'name': 'Голубика', 'image': 'bilberry.webp', 'description': 'Крупная синяя ягода, улучшает память'},
    {'name': 'Смородина чёрная', 'image': 'blackcurrant.webp', 'description': 'Ароматная ягода с высоким содержанием витаминов'},
    {'name': 'Смородина красная', 'image': 'redcurrant.webp', 'description': 'Кисловатая ягода, идеальна для желе'},
    {'name': 'Крыжовник', 'image': 'gooseberry.webp', 'description': 'Зелёная или красная ягода с освежающим вкусом'},
    {'name': 'Вишня', 'image': 'cherry.webp', 'description': 'Сочная косточковая ягода тёмно-красного цвета'},
    {'name': 'Черешня', 'image': 'sweet_cherry.webp', 'description': 'Сладкая крупная ягода, родственница вишни'},
    {'name': 'Облепиха', 'image': 'sea_buckthorn.webp', 'description': 'Оранжевые ягоды, очень богаты витаминами'},
    {'name': 'Клюква', 'image': 'cranberry.jpg', 'description': 'Кислая красная ягода, растёт на болотах'},
    {'name': 'Брусника', 'image': 'lingonberry.webp', 'description': 'Мелкие красные ягоды с горьковатым привкусом'},
    {'name': 'Шелковица', 'image': 'mulberry.webp', 'description': 'Сладкие ягоды белого, красного или чёрного цвета'},
    {'name': 'Боярышник', 'image': 'hawthorn.webp', 'description': 'Красные ягоды, полезные для сердца'},
    {'name': 'Ирга', 'image': 'serviceberry.webp', 'description': 'Сине-фиолетовые ягоды со сладким вкусом'},
    {'name': 'Жимолость', 'image': 'honeysuckle.webp', 'description': 'Вытянутые синие ягоды с уникальным вкусом'},
    {'name': 'Арония', 'image': 'chokeberry.webp', 'description': 'Чёрные ягоды с терпким вкусом'},
    {'name': 'Калина', 'image': 'viburnum.webp', 'description': 'Красные горькие ягоды, полезные при простуде'},
    {'name': 'Рябина', 'image': 'rowan.webp', 'description': 'Оранжево-красные ягоды, становятся сладкими после заморозков'},
    {'name': 'Бузина', 'image': 'elderberry.jpg', 'description': 'Тёмно-фиолетовые ягоды, используются в медицине'},
    {'name': 'Шиповник', 'image': 'rose_hip.jpg', 'description': 'Плоды розы, рекордсмен по содержанию витамина C'},
    {'name': 'Инжир', 'image': 'fig.jpg', 'description': 'Сладкие плоды с множеством мелких семян внутри'},
    {'name': 'Гранат', 'image': 'pomegranate.webp', 'description': 'Крупный плод с множеством сочных зёрен'}
    ]
    
@lab2.route('/lab2/berries')
def berries():
    return render_template('lab2/berries.html', berries=berries_list)