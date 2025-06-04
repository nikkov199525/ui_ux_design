from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    store_link = db.Column(db.String(255), nullable=False)
    access_vision = db.Column(db.String(16), nullable=False)        # none, partial, full
    vision_detail = db.Column(db.Text, nullable=True)
    issues = db.Column(db.Text, nullable=True)
    solutions = db.Column(db.Text, nullable=True)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'))
