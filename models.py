"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def connect_db(app):
    db.init_app(app)


class User(db.Model):
    """Blog User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(200), nullable=True, default="default-user.png")

    def __repr__(self):
        """Show info about user"""
        u = self
        return f"<User.id={u.id} first_name={u.first_name} last_name={u.last_name} avatar={u.avatar}>"

    @property
    def full_name(self):
        """Return the full name of the user"""
        u = self
        return f"{u.first_name} {u.last_name}"


class Post(db.Model):
    """Blog post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    author = db.relationship("User", backref="posts")

    tags = db.relationship(
        "Tag", secondary="posttags", backref=db.backref("posts", lazy="dynamic")
    )

    def __repr__(self):
        """Return Post info"""
        p = self
        return f"<Post.id={p.id} title={p.title} author={p.author.full_name}>"


class Tag(db.Model):
    """Tags for posts"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        """Return tag"""
        return f"<Tag.id={self.id} name={self.name}>"


class PostTag(db.Model):
    """Join posts with tags"""

    __tablename__ = "posttags"

    post_id = db.Column(
        db.Integer, db.ForeignKey("posts.id"), nullable=False, primary_key=True
    )
    tag_id = db.Column(
        db.Integer, db.ForeignKey("tags.id"), nullable=False, primary_key=True
    )
