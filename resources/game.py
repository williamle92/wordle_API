from flask import jsonify,request
from flask_restful import Resource, reqparse
from models.game import Game
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User



class GameResource(Resource):
    @jwt_required()
    def get(self, id):
        current_user = get_jwt_identity()
        game = Game.query.filter_by(creator_id=current_user,id=id).first()
        print(game)
        if game:
            return game.json(), 200
        return {"Message": "The game ID associated with your account could not be found. Please try Again"}, 404

    
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        print(user.json())
        print(user.guesses)
        
        if user:
            game = Game(creator_id =user.id)
            game.users.append(user)
  
            try:
                game.save_to_db()
            except:
                {"Message": "An error occured while processing your request"}, 500
            return game.json(), 201
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
        current_user = get_jwt_identity()
        games = Game.query.filter_by(creator_id=current_user).all()
        return {"type": "games", "data": [game.json() for game in games]}
