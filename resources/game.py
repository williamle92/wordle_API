from flask_restful import Resource, reqparse
from models.game import Game
from flask_jwt_extended import jwt_required

from models.user import User


class GameResource(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument("user_id", type=int, required=True, help="Must contain a User ID")
    @jwt_required()
    def get(self, id):
        game = Game.find_by_id(id)
        if game:
            return game.json()
        return {"Message": "The game ID could not be found. Please try Again"}, 404

    
    @jwt_required()
    def post(self, username):
        user = User.query.filter_by(username=username).first()
        
        if user:
            game = Game(creator_id =user.id)
            print(game.wordle_answer)
            try:
                game.save_to_db()
            except:
                {"Message": "An error occured while processing your request"}, 500
            return "hello world"
        return {"Message": "please include a username with your request"}

    
    @jwt_required()
    def put(self,id):
        data = GameResource
        game = Game.find_by_id(id)

        if game is None:
            game = Game()
        else:
            game.users = data["users"]
            game.status = data['status']
        game.save_to_db
        return game.json()


class Games(Resource):
    @jwt_required()
    def get(self):
        return {"type": "games", "data": [game.json() for game in Game.query.all()]}
