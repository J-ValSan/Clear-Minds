from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb


app = Flask(__name__)
app.config['MySQL_HOST'] = 'localhost'
app.config['MySQL_USER'] = 'root'
app.config['MySQL_PASSWORD'] = ''
app.config['MySQL_DB'] = 'app_citas'
app.config['MySQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
	return render_template('contenido.html')

@app.route('/layout', method = ["GET", "POST"])
def layout():
	session.clear()
	return render_template("contenido.html")


@app.route('/login', method= ["GET", "POST"])
def login():
	if request.method == "POST":
		email = request.form['email']
		password = request.form['password']

		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM users WHERE email=%s",(email))
		user = cur.fetchone()
		cur.close()

		if len(user)>0:
			if password == user["password"]:
				session['name'] = user['name']
				session['email'] = user['email']
				session['tipo'] = user['id_tip_usu']

				if session['tipo'] == 1:
					return render_template("premiun/home.html")
				elif sesion['tipo'] == 2:
					return render_template("estandar/homeTwo.html")
			else:
				return "Error, Correo o contraseña no valida"
		else:
			return "No existe el usuario"
	else:
		return render_template("login.html")

@app.route('/registro', method = ["GET", "POST"])
def registro():

	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM tip_usu")
	tipo = cur.fetchall()

	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM sexo_interes")
	interes = cur.fetchall()
	cur.close()

	if request == 'GET':
		return render_template("registro.html", tipo = tipo , interes = interes)

	else:
		name = request.form['name']
		email.request.form['email']
		password = request.form['password']
		tip = request.form['tipo']
		interes = request.form['interes']

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users(name, email, password, id_tip_usu, interes) VALUES (%s, %s, %s, %s, %s)", (name, email, password, tip, interes))
		mysql.connection.commit()
		return redirect(url_for('login.html'))


if __name__ == '__main__':
	app.run(debug=True)