from flask_restful import Resource, reqparse
from models.guess import Guess



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

    def post(self):
        data = GuessResource.parser.parse_args()
        
        guess = Guess(**data)
        guess.save_to_db
        return {"Message": "Successfully created a guess"}, 200