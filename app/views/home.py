from flask import Blueprint, render_template, redirect, url_for
from ..config import db, login_manager, bootstrap
from ..models import User
from flask.ext.login import (login_user, logout_user, 
                             current_user, login_required)
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

home = Blueprint('home', __name__)

@home.route('/')
def home_page():
    return render_template('home/home.html')

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@home.route("/login", methods=["GET", "POST"])
def login():
        """For GET requests, display the login form. For POSTS, login the current user
        by processing the form."""
        print db
        if current_user.is_authenticated:
            return redirect(url_for("dashboard.dashboard_page"))
        form = LoginForm()
        error = ""
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    login_user(user, remember=form.remember_me.data)
                    return redirect(url_for("dashboard.dashboard_page"))
            error = "Invalid email or password"
        return render_template("home/login.html", form=form, error=error)

@home.route("/logout", methods=["GET"])
@login_required
def logout():
        """Logout the current user."""
        user = current_user
        user.authenticated = False
        db.session.add(user)
        db.session.commit()
        logout_user()
        return render_template("home/logout.html")

@home.route("/register", methods=["GET", "POST"])
def register():
        """For GET requests, display the login form. For POSTS, login the current user
        by processing the form."""
        print db
        form = RegisterForm()
        if form.validate_on_submit():
            user = User(form.username.data, form.email.data, 
                        generate_password_hash(form.password.data))
            print "Inserting into users."
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for("dashboard.dashboard_page"))
        return render_template("home/signup.html", form=form)

#@home.route("/profile/<username>")
