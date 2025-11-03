from flask import Flask, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/lab1/web")
def start():
    return """<!doctype html>" \
        "<html>" \
        "   <body>" \
        "       <h1>web-сервер на flask</h1>" \
                <a href="/lab1/author">Перейти к информации об авторе</a>
        "   </body>" \
        "</html>"""

@app.route("/lab1/author")
def author():
    name = "Сопова Виктория Андреевна"
    group = "ФБИ-31"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Группа: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route('/lab1/image')
def image():
    path = url_for("static", filename="oak.jpg")
    return '''
<!doctype html>
<html>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''