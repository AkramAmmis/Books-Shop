from .resources import UsersResource
from flask_restful import Api

api=Api()

api.add_resource(UsersResource,'/api/users')