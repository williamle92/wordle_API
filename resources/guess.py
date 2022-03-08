from flask_restful import Resource, reqparse
from models.guess import Guess
from models.game import Game
from generateword import english_5_letter_words
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User


class GuessResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("guess", type=str, 
                        required=True,
                        help="Must contain key: guess and value (a 5 letter word)")

    parser.add_argument('game_id',
                        type=int,
                        required=True,
                        help="Must contain a game ID"
                        )

    @jwt_required()
    def post(self):
        data = GuessResource.parser.parse_args()
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        game = Game.query.filter_by(id=data['game_id']).first()
        if not game:
            return {"The game ID you entered does not exist"}, 400
        # check to see if user exists and the game with the game id exists
        if user and game:
            # Check to see if the game is linked to the user
            if user in game.users:
                # instantiating the guess object with data parsed from reqparse
                guess = Guess(guess=data['guess'].upper(), user_id=user.id)
                guess.wordle_answer = game.wordle_answer
                # first check to see if the guess was accurate
                if guess.accuracy == True or guess.guess == game.wordle_answer:
                    game.status = "Solved"
                    game.attempts += 1
                    game.save_to_db()
                    return {"Message": "Congratulations! You have solved this wordle challenge."}
                # check to see if the game has been solved already
                if game.status == "Solved":
                    return {"Message": "This game has already been solved, please create a new game if you would like to play"},
                # checks to see the status of the game before proceeding
                if game.guesses_left == 0 or game.status == "Closed":
                    game.status = "Closed"
                    game.save_to_db()
                    return {"Message": "This game is closed. You ran out of guesses!", "answer": guess.wordle_answer}

                # validates the guess to make sure it is from the dictioanry and the length is 5 letters
                if guess.guess not in english_5_letter_words or len(guess.guess) != 5:
                    return {"Message": "Please use a 5-letter word from the English dictionary"}, 404
                else:
                    game.attempts += 1
                    guess.save_to_db()
                    game.guesses.append(guess)
                    game.save_to_db()

                return {"Message": "Successfully created a guess", "guess": {"data": guess.json()}, "game": {"data": game.json()}}, 200
        return {"Message": "You do not have access to the game, please enter a game ID that belongs to your account"}, 401



    @jwt_required()
    def get(self, id):
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        guess = Guess.query.filter_by(id=id, user_id=user.id).first()
        if not guess:
            return {"Message": "Invalid guess ID or user does not have access to this guess"}, 400
        else:
            return guess.json(),200 
