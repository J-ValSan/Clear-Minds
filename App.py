from flask import Flask, render_template
App = Flask(__name__)

@App.route("/")
def index():
    return render_template("index.html")

@App.route("/Game")
def index2():
    return "<h1>Game</h1>"

@App.route("/Name/<string:nombre>")
def Name(nombre):
    return "Aqui presentaremos un ingreso del usuario"

if __name__ == "__main__":
    App.run(debug=True)