import re

from flask import Flask, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect


app = Flask(__name__)
app.secret_key = "This is my secret Key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'app_cm'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SESSION_TYPE'] = 'filesystem'
mysql = MySQL(app)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if len(user) > 0:
            if password == user["password"]:
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("principal.html")
            else:
                return "Error, Correo o contraseña no valida"
        else:
            return "No existe el usuario"
    else:
        return render_template("login.html")


@app.route('/registro', methods=["GET", "POST"])
def registro():

    if request.method == "GET":
        return render_template("registro.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users(name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        return redirect(url_for('login'))


@app.route('/principal', methods=['GET', 'POST'])
def principal():
    return render_template('principal.html')


@app.route('/fuentes', methods=['GET', 'POST'])
def fuentes():
    return render_template('fuentes.html')


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/preguntasJuntas/<enfermedad>/', methods=['POST', 'GET'])
def resultJunto(enfermedad):

    file = open(f"static/preguntas_{enfermedad}.txt", encoding="utf-8")
    lineas = file.readlines()
    file.close()

    if(request.method == 'POST'):

        exp = 0
        val = 0
        resultado = {}

        for id in range(len(lineas)):

            if id not in resultado:
                resultado[id] = []

            respuestaCorrecta_id = request.form.get("correcta-"+str(id))
            respuestaSelecta_id = request.form.get("respuesta-"+str(id))

            if(respuestaSelecta_id == None):
                return redirect("/preguntasJuntas/"+enfermedad+"/")

            if(respuestaSelecta_id == respuestaCorrecta_id):
                resultado[id].append(True)
                val += 1
            else:
                resultado[id].append(False)

        # Aqui es donde guardariamos la información en base de datos
        exp = val*10.36
        print(exp)
        return str(exp)

    # Supongamos los archivos estan en /static/
    # y se llama usuario_NOMBRE.txt
    # y su formato es por fila es:
    # 	<PREGUNTA>|<RESPUESTA>|<RESPUESTA>|<RESPUESTA>|<RESPUESTA>|<INDICE_RESPUESTA_CORRECTA>
    # ej:¿Estas Triste?|Si|No|Tal vez|No lo se|1

    preguntas = []
    id = 0
    for linea in lineas:
        data = linea.strip().split("|")
        pregunta = data[0]  # Pregunta
        respuestas = data[1:-1]  # Respuestas
        correcta = data[-1]  # Indice de la respuesta correcta

        # Creamos un diccionario con la pregunta y sus respuestas
        dic = {
            "id": id,
            "pregunta": pregunta,
            "respuestas": respuestas,
            "correcta": correcta
        }

        # Añadimos el diccionario al array de preguntas
        preguntas.append(dic)
        id += 1

    return render_template("preguntasJuntas.html", preguntas=preguntas)



if __name__ == "__main__":
    app.run(debug=True)
