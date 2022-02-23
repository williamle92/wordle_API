from db import db


class Guess(db.Model):
    __tablename__ = "guess"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(5), )