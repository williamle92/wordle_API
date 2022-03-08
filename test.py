from db import db

class Guess(db.Model):
    __tablename__ = "guess"
    id = db.Column(db.Integer, primary_key=True)
    guess = db.Column(db.String(5),nullable=False )
    accuracy = db.Column(db.Boolean, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    wordle_answer = db.Column(db.String(5), db.ForeignKey("game.wordle_answer"), nullable=False)


    def __init__(self, guess, game_id, user_id):
        self.guess = guess
        self.game_id =game_id
        self.user_id = user_id


guess = Guess('audio',14,1)
print(guess.guess, guess.user_id,guess.accuracy)