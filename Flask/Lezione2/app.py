from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    DateTimeField,
    RadioField,
    SelectField,
    TextField,
    TextAreaField,
    SubmitField,
)
from wtforms.validators import DataRequired

# create the app
app = Flask(__name__)
# Set the secret key
app.config["SECRET_KEY"] = "superkey"

# Default Route
@app.route("/")  # 127.0.0.1:5000
def index():
    return render_template("home.html")  # render the basic template


##########################
### Course management


# Custom parameters route
@app.route("/course/<input_name>")
def course_name(input_name):
    name = input_name
    return render_template("flask.html", name=name)


# List of courses
@app.route("/course/")
def course_list():
    user_logged_in = True
    course_list = ["flask", "pygame", "data science", "machine learning"]
    return render_template(
        "courses.html", log_ok=user_logged_in, courses_iter_list=course_list
    )


###############
# New Courses

# Sign up form to compile
@app.route("/course/new/")
def new_course():
    return render_template("course_new.html")


# Thank you page after form compiled
@app.route("/course/created")
def course_created():
    # grab first name variable from signup html page
    course_name = request.args.get("course-name")
    course_subject = request.args.get("course-subject")

    # save to database

    return render_template(
        "course_created.html", course_name=course_name, course_subject=course_subject
    )


###### ERROR HANDLER
## Page 404 error
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


################################################
#### ADVANCE FORMS WITH wtforms and flask_wtf
class InfoForm(FlaskForm):  # Inherit from FlaskForm
    name = StringField("What's the name of the course? ")
    submit = SubmitField("Submit")


# Route for the advance form
@app.route("/course/create/simple/", methods=["GET", "POST"])
def advance_form():
    name = False  # placeholder iniziale
    form = InfoForm()  # Oggetto InfoForm

    # Logic of the form
    if form.validate_on_submit():  # if you press: submit, this is what happend
        name = form.name.data  # get the data
        form.name.data = ""  # reset
    return render_template("course_advance.html", advance_form=form, course_name=name)


################################################
#### SUPER ADVANCE FORMS with validators, session, url for, ...
class CourseAdvanceForm(FlaskForm):
    """Definition of the form

    Args:
        FlaskForm (object): FlaskForm default main class
    """

    course_name = StringField(
        "What's the name of the course", validators=[DataRequired()]
    )
    course_active = BooleanField("The course is active?")
    difficulty = RadioField(
        "Please the difficulty of the course:",
        choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
    )
    platform = SelectField(
        u"Pick the platform you want to do the course:",
        choices=[("zoom", "Zoom"), ("skype", "Skype"), ("teams", "Teams")],
    )
    # the u before the string is the casting to unicode
    note = TextAreaField()
    submit = SubmitField("Submit")


@app.route("/course/create/advance", methods=["GET", "POST"])
def super_form():

    # Actions for the complicate form
    course_form = CourseAdvanceForm()

    # if the form is compiled
    if course_form.validate_on_submit():

        # save form information into session user cookie
        session["course_name"] = course_form.course_name.data
        session["course_active"] = course_form.course_active.data
        session["difficulty"] = course_form.difficulty.data
        session["platform"] = course_form.platform.data
        session["note"] = course_form.note.data

        # reset the form
        course_form.course_name.data = ""
        course_form.course_active.data = ""
        course_form.difficulty.data = ""
        course_form.platform.data = ""
        course_form.note.data = ""

        # go to the thankyou template page (thankyou function in python file)
        return redirect(url_for("course_result"))

    return render_template("course_advance_super.html", form=course_form)


@app.route("/course/create/advance/result")
def course_result():
    flash("Form compiled succesfully!")  # flash an alert message to the user
    return render_template("course_result.html")


## Main function (app run)
if __name__ == "__main__":
    app.run(debug=True)

