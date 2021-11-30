

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb


app = Flask(__name__)
app.secret_key = "This is my secret Key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'app_cm'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SESSION_TYPE'] = 'filesystem'
mysql = MySQL(app)


@app.route('/login', methods= ["GET", "POST"])
def login():
	if request.method == "POST":
		email = request.form['email']
		password = request.form['password']

		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM users WHERE email=%s",(email,))
		user = cur.fetchone()
		cur.close()

		if len(user)>0:
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


@app.route('/registro', methods = ["GET", "POST"])
def registro():

	if request.method == "GET":
		return render_template("registro.html")
	else:
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users(name, email, password) VALUES (%s, %s, %s)", (name, email, password))
		mysql.connection.commit()
		return redirect(url_for('login'))

@app.route('/principal', methods = ['GET' ,'POST'])
def principal():
	return render_template('principal.html')

if __name__ == '__main__':
	app.run(debug=True)