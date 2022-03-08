from db import db
from generateword import possible_wordle_words
import random
from sqlalchemy.ext.hybrid import hybrid_property


guesses = db.Table('guesses',
                   db.Column('guess_id', db.Integer, db.ForeignKey(
                       "guess.id"), primary_key=True),
                   db.Column('game_id', db.Integer, db.ForeignKey(
                       'game.id'), primary_key=True)
                   )


users = db.Table('users',
                 db.Column('user_id', db.Integer, db.ForeignKey(
                     "user.id"), primary_key=True),
                 db.Column('game_id', db.Integer, db.ForeignKey(
                     'game.id'), primary_key=True)
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
        self.attempts = 0



    @hybrid_property
    def guesses_left(self):
        return 6 - len(self.guesses)

    def json(self):
        return {"type": "Game","id": self.id, "attempts": self.attempts, "creator_id": self.creator_id,  "guesses_left": self.guesses_left, "users": [user.username for user in self.users], "previous_guesses": {"guesses_with_context": self.guess_with_context}, "user_guesses": self.guesses_user}

    @hybrid_property
    def guesses_user(self):
        arr = []
        for guess in self.guesses:
            string = f"ID: {guess.user_id} guess: {guess.guess}"
            arr.append(string)
        return arr

    @hybrid_property
    def guess_with_context(self):
        arr_all_words = []
        for word in self.guesses:
            guess_arr = list(word.guess)
            secret_arr = list(self.wordle_answer)
            # Check for the positional letter in each word first and then replace it with green
            for i in range(len(self.wordle_answer)):
                letter = guess_arr[i]
                if letter == secret_arr[i]:
                    guess_arr[i] = f"{letter}: green"
                    secret_arr[i] = "*"
            
            # now we check letters in the word and then replace it with yellow
            for i in range(len(self.wordle_answer)):
                letter = guess_arr[i]
                if "green" in letter:
                    continue
                if letter in secret_arr:
                    guess_arr[i] = f"{letter}: yellow"
                    secret_arr.remove(letter)
            
            # now loops through all the remaining letters and replace it with no match
            for i in range(len(self.wordle_answer)):
                letter = guess_arr[i]
                if len(letter) == 1:
                    guess_arr[i] = f"{letter}: no match"
            arr_all_words.append(guess_arr)
        return arr_all_words


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"id: {self.id}, status: {self.status}, 'guesses' : {self.guesses}"

    @classmethod
    def find_by_id(self, id):
        return Game.query.filter_by(id=id).first()
