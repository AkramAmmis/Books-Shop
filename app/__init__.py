from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_mail import Mail
from flask_session import Session
from flask_migrate import Migrate
from .models import ma, db
from flask_admin import Admin 
from .API import api
from flask_session import Session
import os

admin = Admin()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    global app
    
    app = Flask(__name__)
    
    app.user_images = 'users_data'

    ### environment konfigurationen 
    load_dotenv()
    app.config.from_object('config.settings.Development')

    from .admibp.views import MyAdminIndexView
    
    #### Initialize extensions
    mail = Mail(app)

    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db, command='db')
    admin.init_app(app,index_view=MyAdminIndexView())
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
   

    #from app.models import db
    from .models.model import User,Book
    with app.app_context():
        ### DatenBank erstellen
        db.create_all()
        db.session.commit()
        
        user = User.query.filter_by(id=1).first()
        book = Book.query.filter_by(id=8).first()
        ### Fehlerbehandlung
        '''
        @app.errorhandler(Exception)
        def handel_exception(e):
            return f'Ein Fehler ist aufgetreten : {e}'
        '''
        @app.errorhandler(404)
        def not_found(e):
            return 'Diese Seite wurde nicht gefunden!', 404
        
        ###
        from .models.model import User
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        
        ### Model Views hinzufügen für Admin-Panel

        
        ### Blueprints importieren
        from .views.home import home as home_blueprint
        from .views.auth import auth as auth_blueprint
        from .admibp.views import adminbp as admin_blueprint
        from .views.payment import payment_blueprint as payment_blueprint
        ### Blueprints registrieren
        app.register_blueprint(home_blueprint)
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(admin_blueprint)
        app.register_blueprint(payment_blueprint)
        
        return app