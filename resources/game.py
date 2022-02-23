from flask_restful import Resource, reqparse
from models.game import Game



class GameResource(Resource):
    def get(self, id):
        game = Game.find_by_id(id)
        if game:
            return game.json()
        return {"Message": "The game ID could not be found. Please try Again"}, 404

    def post(self):
        game = Game()
        try:
            game.save_to_db()
        except:
            {"Message": "An error occured while processing your request"}, 500

        return game.json()

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
    def get(self):
        return {"type": "games", "data": [game.json() for game in Game.query.all()]}
