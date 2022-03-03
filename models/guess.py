from db import db
from models.game import Game



class Guess(db.Model):
    __tablename__ = "guess"
    id = db.Column(db.Integer, primary_key=True)
    guess = db.Column(db.String(5),nullable=False )
    accuracy = db.Column(db.Boolean, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    wordle_answer = db.Column(db.String(5), db.ForeignKey("game.wordle_answer"), nullable=False)


    def __init__(self, guess, user_id, game_id):
        self.guess = guess
        self.user_id = user_id
        self.accuracy =  self.check_word(guess)
        self.game_id =game_id


    def check_word(self, word):
        return word == self.wordle_answer

    def guess_hints(self):
        arr = []
        for index, letter in enumerate(self.guess):
            if self.wordle_answer[index] == letter:
                arr.append({letter : "Match-Green"})
            elif letter in self.wordle_answer:
                arr.append({letter: "Match-Yellow"})
            else:
                arr.append({letter: "No Match"})
        return arr


    def json(self):
        return {"id": self.id, "game id": self.game_id, "guess": self.guess, "accurate": self.accuracy, "guess hints": self.guess_hints(self.guess)}

    def _repr__(self):
        return f"word : {self.guess}, accuracy: {self.accuracy}"


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()