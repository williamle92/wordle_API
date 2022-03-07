from flask_restful import Resource, reqparse
from models.guess import Guess
from models.game import Game
from generateword import english_5_letter_words
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User

class GuessResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("guess", type=str, required=True, help="Must contain key: guess and value (a 5 letter word)")
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="Must contain a user ID"
                        )
    parser.add_argument('game_id',
                        type=int,
                        required=True,
                        help="Must contain a game ID"
    
                        )


    @jwt_required()
    def post(self):
        data = GuessResource.parser.parse_args()
        print(data)
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        game = Game.query.filter_by(id=data['game_id']).first()
        print(user)
        print(game)
        if user and game:
            if user.username in game.users:
                guess = Guess(user_id=user.id, game_id = data['game_id'], guess=data['guess'])
                if guess.guess not in english_5_letter_words and len(guess.guess) != 5:
                    return {"Message": "Please use an actual 5-letter word from the English dictionary"}, 404
                else:
                    game.guesses.append(guess)
                    game.save_to_db()
                    guess.save_to_db
                return {"Message": "Successfully created a guess", "data": {"guess " : guess.json(), "game": game.json()}}, 200
        return {"Message": "You do not have access to the game, please enter a game ID that belongs to your account"}, 401