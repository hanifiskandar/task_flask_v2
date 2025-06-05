from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User
from app.forms.auth_form import RegistrationForm, LoginForm
from app import db, bcrypt
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

@auth_bp.route("/register",methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("task.list_tasks"))
        flash("Invalid username or password", "danger")
    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout",methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
