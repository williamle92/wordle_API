from flask_marshmallow import Marshmallow

ma = Marshmallow()



class UserSchema(ma.Schema):
    fields = ('username', )