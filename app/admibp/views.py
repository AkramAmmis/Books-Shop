from flask import Blueprint,redirect,url_for,flash
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from app import admin
from ..models.model import User, Book
from ..models import db
from werkzeug.security import generate_password_hash
adminbp = Blueprint('adminbp', __name__)


class UserModelView(ModelView):
    def on_model_change(self, form, model, is_created):
         model.password = generate_password_hash(password=form.password.data,method='sha256')

class myModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.email=='akramammis0@gmail.com'
    
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
            return current_user.is_authenticated and current_user.email=='akramammis0@gmail.com'
    
admin.add_view(UserModelView(User, db.session))
admin.add_view(myModelView(Book, db.session))