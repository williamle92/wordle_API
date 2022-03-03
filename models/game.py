from db import db
from generateword import answer


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    wordle_answer = db.Column(db.String(5), nullable=False, unique=True)
    guesses_left = db.Column(db.Integer)
    status = db.Column(db.String(20))
    guesses = db.relationship('Guess', backref="game", lazy="dynamic")
    
    guesses_left = 6 -len()
    status = "Open"

    def __init__(self, user_id):
        self.guess_with_context = []
        self.guess_with_user = []
        self.wordle_answer = answer
        self.user_id = user_id
       

    def json(self):
        return {"type": "Game", "id": self.id, "guesses_left": self.guesses_left, "status": self.status, "users": [user.json() for user in self.users.all()], "guesses": [guess.json() for guess in self.guesses.all()], "user guess": self.guess_with_user, "guess with context": self.guess_with_context}

    def guess_with_user(self, word, user):
        self.guess_with_user.append({"guess": word, "user": user})

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

    @classmethod
    def find_by_id(self, id):
        return Game.query.filter_by(id=id).first()
