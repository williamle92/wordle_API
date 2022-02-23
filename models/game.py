from sqlalchemy import Integer
from db import db
from generateword import *

class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    wordle_answer = db.Column(db.String(5), nullable=False, unique=True)
    guesses_left = db.Column(db.Integer)
    guesses = db.relationship('Guess', backref="game", lazy="dynamic")
    users = db.relationship('User', backref="game", lazy="dynamic")
    status = db.Column(db.String(20))


    def __init__(self):
        self.wordle_answer = answer
        self.guesses_left = 6
        self.status = "Open"


    def changeGameStatus(self):
        if self.guesses_left == 0:
            self.status = "Complete"
    
    def removeGuess(self):
        self.guesses_left -= 1
