from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/esempio/")
def esempio():
    return render_template("flask.html")

@app.route("/course/<name>")
def course_flask(name):
    lista_corsi = ["flask","pygame","data science","python base"]
    return render_template("corso-flask.html",nome_corso=name,pagina_lista_corsi=lista_corsi)


@app.route("/info/")
def info_2_test():
    return f"<h2>Queste sono un sacco di informazioni!<h2>"

@app.route("/info/<name>") #127.0.0.1:5000/info/andrea
def nome_ok(name):
    return f"<h2>Il mio nome: {name} <h2>"

@app.route("/info-errore/<name>")
def errore(name):
    stringa = f"<h2>Generiamo un errore:<h2>".format(name[50])
    return stringa

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errore.html"), 404

if __name__ == "__main__":
    app.run(debug=True)