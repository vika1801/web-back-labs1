from flask import Blueprint, redirect, url_for, render_template, request, make_response
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name',"Незнакомец")
    age = request.cookies.get('age', 'Неизвестен') 
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name','Alex', max_age=5)
    resp.set_cookie('age','20')
    resp.set_cookie('name_color','magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors={}
    user = request.args.get('user')
    if user == '':
        errors['user']  = 'Заполните поле!!!'
    age = request.args.get('age')
    if age == '':
        errors['age']  = 'Заполните поле!!!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
      return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
      price=0
      drink = request.args.get('drink')
      if drink == 'coffee':
            price = 120
      elif drink == 'black-tea':
            price = 80
      else:
            price = 70

      if request.args.get('milk') == 'on':
            price += 30
      if request.args.get('sugar') == 'on':
            price += 10

      return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    font_size = request.args.get('font_size')
    background_color = request.args.get('background_color')
    if color or font_size or background_color:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if background_color:
            resp.set_cookie('background_color', background_color)
                    
        return resp
    else:
        color = request.cookies.get('color', 'rgb(14, 75, 101)')
        font_size = request.cookies.get('font_size', '18')
        background_color = request.cookies.get('background_color', 'white')
        resp = make_response(render_template('lab3/settings.html',color=color,font_size=font_size,background_color=background_color))
        return resp


@lab3.route('/lab3/train_ticket')
def train():
    errors={}
    pass_name = request.args.get('pass_name')
    shelf = request.args.get('shelf')
    with_bed = request.args.get('with_bed')
    with_luggage = request.args.get('with_luggage')
    age = request.args.get('age')
    from_t = request.args.get('from_t')
    to_t = request.args.get('to_t')
    travel_date = request.args.get('travel_date')
    insurance = request.args.get('insurance')

    if pass_name and shelf and age and from_t and to_t and travel_date:
        age = int(age)
        
        ticket_price = 1000 if age >= 18 else 700  

        if shelf in ['low', 'low_side']:
            ticket_price += 100
        if with_bed == 'on':
            ticket_price += 75
        if with_luggage == 'on':
            ticket_price += 250
        if insurance == 'on':
            ticket_price += 150

        ticket_type = "Детский билет" if age < 18 else "Взрослый билет"

        return render_template('lab3/ticket.html', 
                               pass_name=pass_name, 
                               ticket_type=ticket_type,
                               ticket_price=ticket_price,
                               from_t=from_t,
                               to_t=to_t,
                               travel_date=travel_date)

    return render_template('lab3/train.html')