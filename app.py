"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session

from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False  # Disable redirect interception

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:Bu11fr09@localhost:5432/blogly"
)
app.config["SECRET_KEY"] = "yomama"
app.config["SQLALCHEMY_ECHO"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
@app.route("/users/", methods=["GET", "POST"])
def list_users():
    """List blog users"""

    users = User.query.order_by("last_name")
    return render_template("index.jinja-html", users=users)


@app.route("/users/new", methods=["GET"])
def add_user_form():
    """Add user"""

    return render_template("add-user.jinja-html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Save new user to database"""
    try:
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        avatar = request.form["avatar"]

        new_user = User(first_name=first_name, last_name=last_name, avatar=avatar)

        db.session.add(new_user)
        db.session.flush()  # Flush the session to generate the ID without committing
        logging.info(f"New user ID (before commit): {new_user.id}")

        db.session.commit()

        return redirect(f"/users/{new_user.id}")
    except Exception as e:
        db.session.rollback()
        return str(e), 500


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Display user details"""

    user = User.query.get_or_404(user_id)

    return render_template("user.jinja-html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user(user_id):
    """Edit user form"""

    user = User.query.get_or_404(user_id)

    return render_template("edit-user.jinja-html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """Edit user form"""

    user = User.query.get_or_404(user_id)
    try:
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.avatar = request.form["avatar"]

        db.session.commit()
        return redirect(f"/users/{user.id}")
    except Exception as e:
        db.session.rollback()
        return str(e), 500


@app.route("/users/<int:user_id>/delete", methods=["GET"])
def delete_user(user_id):
    """Delete user"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users/")
