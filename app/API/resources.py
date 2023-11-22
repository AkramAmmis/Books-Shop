from flask_restful import Resource
from app.models.model import User, users_schema,user_schema


class UsersResource(Resource):
    def get(self):
         user = User.query.all()
         print(user)
         return users_schema.dump(user)