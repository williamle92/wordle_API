from db import db
from sqlalchemy.ext.hybrid import hybrid_property


class Guess(db.Model):
    __tablename__ = "guess"
    id = db.Column(db.Integer, primary_key=True)
    guess = db.Column(db.String(5),nullable=False )
    accuracy = db.Column(db.Boolean, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    wordle_answer = db.Column(db.String(5), db.ForeignKey("game.wordle_answer"), nullable=False)


    def __init__(self, guess, user_id):
        self.guess = guess
        self.user_id = user_id

    @hybrid_property
    def accuracy(self):
        return self.guess == self.wordle_answer


    @hybrid_property
    def guess_hints(self):
        guess_arr = list(self.guess)
        secret_arr = list(self.wordle_answer)
        # checking for positional letter in guess
        for i in range(len(self.guess)):
            letter = guess_arr[i]
            if letter == secret_arr[i]:
                guess_arr[i] = f"{letter}: green"
                secret_arr[i] = "*"
        # checking for letters in the secret word
        for i in range(len(self.guess)):
            letter = guess_arr[i]
            if "green" in letter:
                continue
            
            if letter in secret_arr:
                guess_arr[i] = f"{letter}: yellow"
                secret_arr.remove(letter)

            # loop through remaining letters and replace it with no match
            for i in range(len(self.guess)):
                letter = guess_arr[i]
                if len(letter) == 1:
                    guess_arr[i] = f"{letter}: no match"
        return guess_arr


    def json(self):
        return {"id": self.id, "guess": self.guess, "accuracy": self.accuracy, "guess_hints": self.guess_hints}

    def _repr__(self):
        return f"guess : {self.guess}"


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()