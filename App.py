from flask import Flask, render_template
App = Flask(__name__)

@App.route("/")
def index():
    return render_template("index.html")
#xd
@App.route("/Game")
def index2():
    return "<h1>Game</h1>"
#xd
@App.route("/Name/<string:nombre>")
def Name(nombre):
    return "Aqui logeamos a un usuario"
#Linea de Logeo#

if __name__ == "__main__":
    App.run(debug=True)
    
    
 # hola buenas xdxdxd
