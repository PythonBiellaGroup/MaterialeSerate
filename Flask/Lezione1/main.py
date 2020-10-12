from flask import Flask, render_template, request, session, redirect, url_for, flash

# create the app
app = Flask(__name__)
# Set the secret key
app.config["SECRET_KEY"] = "superkey"

# 1. Default Route
@app.route("/")  # 127.0.0.1:5000
def index():
    return render_template("home.html")  # render the basic template


# 2. Custom Basic Route
@app.route("/info")  # 127.0.0.1:5000/info
def info():
    wow = "beautiful"
    return f"<h1> Hello {wow} World!<h1>"


# 3. Custom parameters route
@app.route("/course/<name>")
def course_name(name):
    return f"<h2>Nome del tuo corso: {name}</h2>"


# 4. Error debug
@app.route("/error/<name>")
def course_error(name):
    return "<h2>Nome del tuo corso {}</h2>".format(name[100])


# 5. Single Course informations
@app.route("/course/flask")
def course_flask():
    return render_template("flask.html")


# 6. Jinja Iterators Route usage
@app.route("/course/")
def course_list():
    user_logged_in = True
    course_list = ["flask", "pygame", "data science", "machine learning"]
    return render_template(
        "courses.html", log_ok=user_logged_in, courses_iter_list=course_list
    )


## Page 404 error
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


## Main function (app run)
if __name__ == "__main__":
    app.run(
        debug=True
    )  # use the debug (you can use the pin in terminal to debug on webpage)
