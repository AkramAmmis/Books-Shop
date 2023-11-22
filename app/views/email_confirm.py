from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from flask_mail import Mail, Message
from ..models.model import User
from ..models import db
from .. import app

mail = app.extensions['mail']

serializer = URLSafeTimedSerializer('keyforthisapp')
sender = app.config['MAIL_USERNAME']

def token(email,proc):
    #create token and send msg for confirm
    token = serializer.dumps(email,salt='confirm-email')
    
    url = url_for(f'{proc}.confirm', token=token , _external=True)
   
    msg = Message('Ammis - Confirm Email', recipients=[email], sender=sender)
    msg.body = f'pless confirm your email from heir : <a href="{url}" target="_blank">click here</a>'
    mail.send(msg)
    print('wird gemacht', url)


                      #um entscheiden zu können, ob True oder False in DB
def check_token(token,create):
    try:
        de_token = serializer.loads(token, salt='confirm-email', max_age=60)
        if create:
            user = User.query.filter_by(email=de_token).first()
            user.confirm_on = True
            db.session.commit()
            return True
        else:
            return True
    except:
        return False
     