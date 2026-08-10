from flask import redirect, url_for, Blueprint, render_template

main_bp = Blueprint("main_bp", __name__, url_prefix="/main")

@main_bp.route("home")
def home():
    return render_template("home.html")