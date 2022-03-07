from db import db
from generateword import possible_wordle_words
import random
from sqlalchemy.ext.hybrid import hybrid_property


guesses = db.Table('guesses', 
db.Column('guess_id', db.Integer, db.ForeignKey("guess.id"), primary_key=True), 
db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)


users = db.Table('users',
db.Column('user_id', db.Integer, db.ForeignKey("user.id"), primary_key=True), 
db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    wordle_answer = db.Column(db.String(5), nullable=False, unique=True)
    creator_id = db.Column(db.Integer)
    attempts = db.Column(db.Integer)
    status = db.Column(db.String(20))
    guesses = db.relationship(
        'Guess', secondary=guesses, backref=db.backref('game_id', lazy="dynamic"))
    users = db.relationship('User', secondary=users,
                            backref=db.backref('game_id', lazy="dynamic"))
    guesses_left = db.Column(db.Integer)

    # On instantiating you would want a new word

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
        return {"type": "Game", "creator_id": self.creator_id,  "id": self.id, "guesses_left": self.guesses_left, "clues": {"guesses_with_context": self.guess_with_context}}

    # def guess_with_user(self):
    #     arr = []
    #     arr.append({"guess": self., "user id": user})

    @hybrid_property
    def guess_with_context(self):
        arr_all_words = []
        for word in self.guesses:
            arr = []
            for i, letter in enumerate(word):
                if letter == self.wordle_answer[i]:
                    arr.append((letter, "green"))
                if word[i] in self.wordle_answer:
                    arr.append((letter, "yellow"))
                else:
                    arr.append((letter, "no match"))
            arr_all_words.append(arr)
        return arr_all_words

    def changeGameStatus(self):
        if self.guesses_left == 0:
            self.status = "Complete"

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
