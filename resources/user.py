from flask_restful import Resource, reqparse
from models.user import User


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Must contain a username"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="Can not register without an email"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Must contain a password"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            return {"Message": "There is already an existing username, please try again with different username"}, 400

        user = User(**data)
        user.save_to_db()
        return {"Message": "User created successfully", "data": user.json()}, 201

class UserResource(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            return user.json(), 200
        return {"Message": "The user searched by user ID does not exist"}, 400
    