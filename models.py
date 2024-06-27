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
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    avatar = db.Column(
        db.String(200), nullable=True, unique=False, default="default-user.png"
    )

    def __repr__(self):
        """Show info about pet"""
        u = self
        return f"<User.id={u.id} first_name={u.first_name} last_name={u.last_name} avatar={u.avatar}>"

    @property
    def full_name(self):
        """Return the full name of the user"""

        u = self
        return f"{u.first_name} {u.last_name}"
