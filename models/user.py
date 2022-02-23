from enum import unique
from db import db



class User(db.Model):
    ''''
    User Model
    Represent users and contained in table: user
    '''

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True,nullable=False)
    guesses_left = db.Column(db.Integer)
    games = db.relationship('Game', backref="user", lazy="dynamic")
    password = db.Column(db.Text(), nullable= False)


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    # Method to save to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {"type": "user","id":self.id , "username":self.username, "email": self.email }

    def __repr__(self):
        return f"username: {self.username} email: {self.email}" 

