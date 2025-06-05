from flask import Blueprint, render_template

index_bp = Blueprint("index", __name__)

@index_bp.route("/")
def home():
    return render_template("index.html", title="Home Page")

@index_bp.route("/about")
def about():
    return render_template("about.html", title="About Parameter Here")
