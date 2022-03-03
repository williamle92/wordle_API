from flask_restful import Resource, reqparse
from models.user import User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required

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
        user = User.query.filter_by(id=id).first()
        if user:
            return user.json(), 200
        return {"Message": "The user searched by user ID does not exist"}, 400
    