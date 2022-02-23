from sqlalchemy import null
from db import db
from generateword import *


class Guess(db.Model):
    __tablename__ = "guess"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(5),nullable=False )
    accuracy = db.Column(db.Boolean, nullable = False)
    game_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    wordle_answer = db.Column(db.String(5), db.ForeignKey("game.wordle_answer"), nullable=False)


    def __init__(self, word, user_id, game_id):
        self.word = word
        self.user_id = user_id
        self.accuracy =  self.check_word(word)
        self.game_id =game_id

    def check_word(self, word):
        return word == self.wordle_answer


    def _repr__(self):
        return f"word : {self.word}, accuracy: {self.accuracy}"


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()