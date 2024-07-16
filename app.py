"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag
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


@app.route("/users/", methods=["GET", "POST"])
def list_users():
    """List blog users"""

    users = User.query.order_by("last_name")
    return render_template("users.jinja-html", users=users)


@app.route("/")
@app.route("/posts/")
def list_posts():
    """List posts"""

    posts = Post.query.order_by("title").all()
    return render_template("index.jinja-html", posts=posts)


@app.route("/users/new", methods=["GET"])
def add_user_form():
    """Add user"""

    return render_template("add-user.jinja-html")


@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def add_post_form(user_id):
    """Add post form"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("add-post.jinja-html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Save new post to database"""

    try:
        title = request.form["title"]
        body = request.form["body"]
        tag_ids = request.form.getlist("tags")
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        new_post = Post(title=title, body=body, author_id=user_id)
        new_post.tags = tags

        db.session.add(new_post)
        db.session.commit()

        return redirect(f"/posts/{new_post.id}")
    except Exception as e:
        db.session.rollback()
        return str(e), 500


@app.route("/users/new", methods=["POST"])
def add_user():
    """Save new user to database"""
    try:
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        avatar = request.form["avatar"]

        new_user = User(first_name=first_name, last_name=last_name, avatar=avatar)

        db.session.add(new_user)

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
    tags = Tag.query.all()
    return render_template("edit-user.jinja-html", user=user, tags=tags)


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


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    """Display post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("post.jinja-html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def edit_post(post_id):
    """Edit post form"""
    post = Post.query.get_or_404(post_id)
    return render_template("edit-post.jinja-html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Update post"""
    post = Post.query.get_or_404(post_id)
    try:
        post.title = request.form["title"]
        post.body = request.form["body"]
        tag_ids = request.form.getlist("tags")
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        post.tags = tags

        db.session.commit()
        return redirect(f"/posts/{post.id}")
    except Exception as e:
        db.session.rollback()
        return str(e), 500


@app.route("/posts/<int:post_id>/delete", methods=["GET"])
def delete_post(post_id):
    """Delete post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect("/posts/")


@app.route("/tags/")
def list_tags():
    """List tags"""

    tags = Tag.query.order_by("name").all()
    return render_template("tags.jinja-html", tags=tags)


@app.route("/tags/new", methods=["GET"])
def add_tag_form():
    """Add tag form"""

    return render_template("add-tag.jinja-html")


@app.route("/tags/new", methods=["POST"])
def add_tag():
    """Add tag"""

    try:
        name = request.form["name"]

        new_tag = Tag(name=name)

        db.session.add(new_tag)
        db.session.commit()

        return redirect(f"/tags/")
    except Exception as e:
        db.session.rollback()
        return str(e), 500


@app.route("/tags/<int:tag_id>")
def tag_detail(tag_id):
    """Display tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts.all()
    return render_template("tag.jinja-html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit", methods=["GET"])
def edit_tag(tag_id):
    """Edit tag form"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("edit-tag.jinja-html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def update_tag(tag_id):
    """Update tag"""

    tag = Tag.query.get_or_404(tag_id)
    try:
        tag.name = request.form["name"]

        db.session.commit()
        return redirect(f"/tags/{tag.id}")
    except Exception as e:
        db.session.rollback()
        return str(e), 500


@app.route("/tags/<int:tag_id>/delete", methods=["GET"])
def delete_tag(tag_id):
    """Delete tag"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags/")
