from flask_restful import Resource, reqparse
from models.guess import Guess
from models.game import Game
from generateword import english_5_letter_words
from flask_jwt_extended import jwt_required

class GuessResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("word", type=str, required=True, help="Must contain a 5 letter word")
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
        guess = Guess(**data)
        if guess not in english_5_letter_words:
            return {"Message": "Please use an actual word"}

        id = guess.game_id
        game = Game.find_by_id(id)
        game.remove_guess()
        guess.save_to_db
        return {"Message": "Successfully created a guess", "data": {"guess info" : guess.json(), "game status": game.json()}}, 200