from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Define movie database model.
class Movie(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    rating = db.Column(db.Integer)
    butter = db.Column(db.Integer)
    name = db.Column(db.String(150))
    poster = db.Column(db.String(150))

# Define user database model.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    movies = db.relationship('Movie')
