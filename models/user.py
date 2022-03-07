from flask import jsonify
from db import db



class User(db.Model):
    ''''
    User Model
    Represent users and contained in table: user
    '''

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True,nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.Text(), nullable= False)
    guesses = db.relationship('Guess', backref="user", lazy="dynamic")


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    # Method to save to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {"id":self.id , "username":self.username, "email": self.email, 'guesses': [g.guess for g in self.guesses]}

    def __repr__(self):
        return f"id: {self.id}, username: {self.username}, email: {self.email}"

    @classmethod
    def find_by_username(self, username):
        return User.query.filter_by(username=username).first()