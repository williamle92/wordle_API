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

        if game:
            return game.json(), 200
        return {"Message": "The game ID associated with your account could not be found. Please try Again"}, 404

    
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        
        if user:
            game = Game(creator_id =user.id)
            game.users.append(user)
  
            try:
                game.save_to_db()
            except:
                return {"Message": "An error occured while processing your request"}, 500
            return game.json(), 201


    
    @jwt_required()
    def put(self,id):
        current_user = get_jwt_identity()
        game = Game.query.filter_by(creator_id=current_user, id=id).first()
        add = request.get_json().get('add', '')
        remove = request.get_json().get('remove', "")
        user_add = User.query.filter_by(username=add).first()
        user_remove = User.query.filter_by(username=remove).first()

        if not add and not remove:
            return {"Message": "Error! can only add or remove user one at a time. Please use keys 'add': username to add, or 'remove': username to remove a user"}
        if game is None:
            game = Game()
        if add and user_add:
            game.users.append(user_add)
        if remove and user_remove:
            game.users.remove(user_remove)
        game.save_to_db
        return game.json(), 200


    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        game = Game.query.filter_by(creator_id = current_user, id=id).first()
        if game:
            try:
                game.delete_from_db()
            except:
                return {"Message": "You do not have the authorization to delete this game"}, 403
            return {"Message": "The game has successfully been deleted"}, 200
      


class Games(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        games = Game.query.filter_by(creator_id=current_user).all()
        return {"type": "games", "data": [game.json() for game in games]}
