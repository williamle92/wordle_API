from db import db
from generateword import possible_wordle_words
import random
from sqlalchemy.ext.hybrid import hybrid_property
from models.guess import Guess

guesses = db.Table('guesses', db.Column('guess_id', db.Integer, db.ForeignKey(
    "guess.id"), primary_key=True), db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True))
users = db.Table('users', db.Column('user_id', db.Integer, db.ForeignKey(
    "user.id"), primary_key=True), db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True))


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    wordle_answer = db.Column(db.String(5), nullable=False, unique=True)
    creator_id = db.Column(db.Integer)
    attempts = db.Column(db.Integer)
    status = db.Column(db.String(20))
    guesses = db.relationship('Guess', secondary =guesses, backref=db.backref('game_id'))
    users = db.relationship('User', secondary=users, backref=db.backref('game id'))
    guesses_left = db.Column(db.Integer)


    # On instantiating you would want a new world
    def __init__(self, creator_id):
        self.wordle_answer = random.choice(possible_wordle_words)
        self.creator_id = creator_id
        self.status = "Open"
        self.attempts = 6

    # @hybrid_property
    # def guesses(self):
    #     guesses = Guess.query.filter(Guess.game_id.any(id=self.id)).all()
    #     return guesses

    @hybrid_property
    def guesses_left(self):
        return 6 - len(self.guesses)
    
    def json(self):
        return {"type": "Game","creator_id": self.creator_id,  "id": self.id,  "game_id": self.id, "users": self.users, "guesses_left": self.guesses_left}

    # def guess_with_user(self):
    #     arr = []
    #     arr.append({"guess": self., "user id": user})

    def guess_with_context(self):
        for word in self.guesses:
            arr = []
            for i in word:
                if word[i] == self.wordle_answer[i]:
                    arr.append({word[i], "green"})
                if word[i] in self.wordle_answer:
                    arr.append([word[i], "yellow"])
                else:
                    arr.append({word[i], "no match"})
            self.guess_with_context.append(arr)

    def changeGameStatus(self):
        if self.guesses_left == 0:
            self.status = "Complete"

    def removeGuess(self):
        self.guesses_left -= 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"id: {self.id}, status: {self.status}"

    @classmethod
    def find_by_id(self, id):
        return Game.query.filter_by(id=id).first()



