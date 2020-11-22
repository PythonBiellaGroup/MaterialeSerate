from flask import Flask, render_template, url_for, request, session, redirect
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    BooleanField,
    RadioField,
    SelectField,
    TextAreaField,
)
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config["SECRET_KEY"] = "supersafekey"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/esempio/")
def esempio():
    return render_template("flask.html")


@app.route("/course/<name>")
def course_flask(name):
    lista_corsi = ["flask", "pygame", "data science", "python base"]
    return render_template(
        "corso-flask.html", nome_corso=name, pagina_lista_corsi=lista_corsi
    )


@app.route("/info/")
def info_2_test():
    return f"<h2>Queste sono un sacco di informazioni!<h2>"


@app.route("/info/<name>")  # 127.0.0.1:5000/info/andrea
def nome_ok(name):
    return f"<h2>Il mio nome: {name} <h2>"


@app.route("/info-errore/<name>")
def errore(name):
    stringa = f"<h2>Generiamo un errore:<h2>".format(name[50])
    return stringa


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errore.html"), 404


#### Form semplice
@app.route("/course/new/")
def new_course():
    course_name = request.args.get("course-name")
    course_subject = request.args.get("course-subject")
    return render_template(
        "course_new.html", course_name=course_name, course_subject=course_subject
    )


@app.route("/course/created")
def course_created():
    course_name = ""
    course_subject = ""

    return render_template(
        "course_created.html", course_name=course_name, course_subject=course_subject
    )


### FORM AVANZATI
class FormCorsoBase(FlaskForm):
    name = StringField("Nome del corso", validators=[DataRequired()])
    teacher = StringField("Insegnate del corso")
    active = BooleanField("Corso attivo?")
    difficulty = RadioField(
        "Difficoltà del corso:",
        choices=[("facile", "Facile"), ("medio", "Medio"), ("avanzato", "Avanzato")],
    )
    platform = SelectField(
        "Piattaforma online del corso",
        choices=[("teams", "Teams"), ("zoom", "Zoom"), ("meet", "Meet")],
    )
    feedback = TextAreaField()
    submit = SubmitField("Submit")


@app.route("/course/simple/", methods=["GET", "POST"])
def advance_form():
    name = False
    teacher = False
    active = False
    difficulty = False
    platform = False
    feedback = False
    form = FormCorsoBase()

    # Costruire la logica del form
    if form.validate_on_submit():
        session["name"] = form.name.data
        session["teacher"] = form.teacher.data
        session["active"] = form.active.data
        session["difficulty"] = form.difficulty.data
        session["platform"] = form.platform.data
        session["feedback"] = form.feedback.data

        # RESET
        form.name.data = ""
        form.teacher.data = ""
        form.active.data = ""
        form.difficulty.data = ""
        form.platform.data = ""
        form.feedback.data = ""

        return redirect(url_for("course_result"))

    return render_template(
        "course_simple.html",
        course_simple_form=form,
        course_name=name,
        course_teacher=teacher,
        course_active=active,
        course_difficulty=difficulty,
        course_platform=platform,
        course_feedback=feedback,
    )


@app.route("/course/result/")
def course_result():
    return render_template("course_result.html")


if __name__ == "__main__":
    app.run(debug=True)
