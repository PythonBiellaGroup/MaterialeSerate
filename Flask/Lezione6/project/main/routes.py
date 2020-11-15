
from flask import Blueprint, render_template

main_blueprint = Blueprint(
    "main",
    __name__, 
    template_folder="templates",
    static_folder='../static'
)

@main_blueprint.route("/", methods=['GET'])
def index():
    return render_template("index.html")