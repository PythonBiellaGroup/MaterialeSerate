from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    wow = "beautiful"
    return f"<h1> Hello {wow} World!<h1>"


if __name__ == "__main__":
    app.run(debug=True)
