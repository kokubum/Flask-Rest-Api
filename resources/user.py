import sqlite3
from flask_restful import reqparse,Resource
from models.user import UserModel


class UserRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True,help='this field cannot be blank')
    parser.add_argument('password',type=str,required=True,help='this field cannot be blank')

    def post(self):
        data = UserRegistration.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message':'Username already used'},400

        user = UserModel(**data)
        user.save_to_db()

        return({'message':'User created successfuly'}),201  
