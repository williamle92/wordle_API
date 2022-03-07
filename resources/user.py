from flask_restful import Resource, reqparse
from models.user import User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Must contain key 'username' and the username in JSON request body"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="Must contain key 'email' and the email in JSON request body"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Must contain key 'password' and the password in JSON request body"
                        )

  
    def post(self):
        # serialize request
        data = UserRegister.parser.parse_args()
        # check to see if user exists by querying db
        if User.find_by_username(data['username']):
            # if user exist, return message
            return {"Message": "Error! That username is already taken, please try again with different username"}, 400
        # generate a password hash
        pwhash = generate_password_hash(data["password"])

        user = User(username=data["username"], email=data['email'], password=pwhash)
        user.save_to_db()
        return {"Message": "User created successfully", "data": user.json()}, 201

class UserResource(Resource):
    @jwt_required()
    def get(self, id):
        current_user = get_jwt_identity()
        logged_in_user = User.query.filter_by(id=current_user).first()
        user = User.query.filter_by(id=id).first()
        print(user)
        print(logged_in_user)
        if user == logged_in_user:
            return user.json(), 200
        return {"Message": "The ID used must be related to the accout logged in, please try again"}, 401
    