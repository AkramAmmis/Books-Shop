from flask import render_template, Blueprint, request, flash, redirect, url_for, session
from  app.forms.user import Register_Form,Anmeldung_Form, EmailSuchen_Form,codeChecking_form, passChange_Form
from app.models import db
from app.models.model import User
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2.utils import markupsafe
from flask_login import login_required, logout_user, current_user,login_user
from .email_confirm import *
import random, string
from flask_session import Session
from os import rename
from werkzeug.utils import secure_filename

auth = Blueprint('auth', __name__)
markup = markupsafe.Markup

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Anmeldung_Form()
    if request.method == 'GET':
        return render_template('auth/login.html', 
                               title='login',
                               form=form,
                               user = current_user)
    name_email = request.form.get('username')
    password = request.form.get('password')
  
    
    #überprüfen, ob benutzername in der Datenbank ist.
    name = User.query.filter_by(username=name_email).first()
    email = User.query.filter_by(email=name_email).first()
    
    if email:   
         
        check_pass = check_password_hash(pwhash=email.password,password=password)
        if check_pass:
            if email.confirm_on == True:
                login_user(email, remember=True)
                flash('Erfolgreich eingeloggt!', category='success')
                return redirect(url_for('home.profil'))
            else:
                msg = markup(f'Ihr konto ist nicht aktiviert!  <a href="/send_msg_confirm/{name_email}">klicken Sie hier</a>, um die Aktivierungsnachricht zu senden..')
                flash(msg, category='error')
                return redirect(url_for('auth.login'))
        else:   
            flash('Die eingegebenen informationen sind falsch!, versuchen Sie nochmal.', category='error')
            return redirect(url_for('auth.login'))
        
    elif name: 
        check_pass = check_password_hash(pwhash=name.password,password=password)
        if check_pass:
            if name.confirm_on == True:
                login_user(name, remember=True)
                flash('Erfolgreich eingeloggt!', category='success')
                return redirect(url_for('home.profil'))
        else:   
            flash('Die eingegebenen informationen sind falsch!, versuchen Sie nochmal.', category='error')
            return redirect(url_for('auth.login'))
    else:   
            flash('Die eingegebenen informationen sind falsch!, versuchen Sie nochmal.', category='error')
            return redirect(url_for('auth.login'))
        
 
        
        
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = Register_Form()
    if request.method == 'GET':
        return render_template('auth/register.html', 
                               title='register', 
                               form=form,
                                user = current_user)
    
    username = request.form.get('username')
    email = request.form.get('email')
    DateOFbirth = request.form.get('DateOFbirth')
    address = request.form.get('address')
    language = request.form.get('language')
    password0 = request.form.get('password')
    password1 = request.form.get('confirm')
    logo = form.logo.data
    email_check = User.query.filter_by(email=email).first()
    username_check = User.query.filter_by(username=username).first()
    
    if email_check:
        markup = markupsafe.Markup
        err = markup('Die E-Mail ist bereits vorhanden, gehen sie zur <a href="/login">Anmeldung Seite.</a>')
        flash(err, category='error')
        return redirect(url_for('auth.register'))
     
    if username_check:
        flash('Der eingegebene Name wird breits verwendet, Bitte geben Sie einen anderen name ein!', category='error')
        return redirect(url_for('auth.register'))
    
    if password0 == password1:
        if logo : 
            logo_name = form.logo.data.filename
            file_name = secure_filename(logo_name)
            logo.save('app/static/user_logo/' + file_name)
            name_save = username.replace(" ", "") + '.jpg' 
            rename('app/static/user_logo/' + file_name, 'app/static/user_logo/' + name_save)
            new_user = User(username=username, email=email ,DateOFbirth= DateOFbirth,address=address, language=language,logo_name=name_save, password=generate_password_hash(password1,method='pbkdf2:sha256'))
        else:
            new_user = User(username=username, email=email ,DateOFbirth= DateOFbirth,address=address, language=language, logo_name='default_logo.png', password=generate_password_hash(password1,method='pbkdf2:sha256'))
        
        db.session.add(new_user)
        db.session.commit()
        token(email,'auth')
        flash('Registrierung erfolgreich abgeschlossen, prüfen Sie ihre Mailbox. ', category='success')
        return redirect(url_for('auth.login'))
        
    else :
        flash('Passwörter stimmen nicht überein', category='error')
        return redirect(url_for('auth.register'))

@auth.route('/confirm/<token>')
def confirm(token):
    if check_token(token,True) == True:
        flash('Ihr Account wurde aktiviert, Sie können sich einloggen', category='success')
        return redirect(url_for('auth.login'))
    else:
        flash('Der Link ist abgelaufen! Geben Sie die Informationen ein, um die Bestätigungsnachricht erneut zu senden. ', category='error')
        return redirect(url_for('auth.login'))

@auth.route('/send_msg_confirm/<path:email>')
def send_msg_confirm(email):
    token(email,'auth')
    flash('Sie wurde gesendet! Prüfen sie Ihr mailbox.', category='success')
    return redirect(url_for('auth.login'))



@auth.route('/email_suchen', methods=['GET', 'POST'])
def email_suchen():
    form = EmailSuchen_Form()
    if request.method == 'GET': 
        return render_template('/auth/email_suchen.html', form=form,user=current_user)
    email = request.form.get('email')
    check_email = User.query.filter_by(email=email).first()
    
    if check_email:
        if check_email.confirm_on == False:
            flash('Das Konto ist noch nicht aktiviert.', category='error')
            return redirect(url_for('auth.login'))
        else:
            session['email']=email
            code = "".join(random.choice(string.digits)  for _ in range(4))
            check_email.code_pass = generate_password_hash(code,method='pbkdf2:sha256')
            db.session.commit()
            msg = Message('k!m0 - Confirm Email', recipients=[email], sender=app.config['MAIL_USERNAME'])
            msg.body = f'Das ist Der Code [ {code} ], durch ihn Sie neues Passwort erstellen können'
            mail.send(msg)
            flash('Prüfen sie Ihr mailbox.', category='success')
            return redirect(f'/codeChecking')
    else:
        flash('Dises Email wurde nicht gefunden', category='error')
        return redirect(url_for('auth.email_suchen'))


## ich versuce hier zu arbeiten um code(pass-returen) zu eingeben und testen, ob er korrekt ist
@auth.route('/codeChecking' ,methods=['GET', 'POST','PUT']) 
def  codeChecking():     
    form = codeChecking_form()
    email = session.get('email')
    check_email = User.query.filter_by(email=email).first()
    if not email or not check_email.code_pass:
        flash('Geben Sie bitte Ihr Email!',category='error')
        return redirect(url_for('auth.email_suchen'))
    else:
        if request.method == 'GET':
            return render_template('/auth/codeChecking.html', 
                                title='code',
                                user=current_user,
                                form = form)
        code = request.form.get('code')
     
        
        
        if check_password_hash(pwhash=check_email.code_pass, password=code):
            flash('Sie können Ihr passwort verändern', category='success')
            check_email.code_pass = 'allowed' #Das heißt kann mann pass_change erreichen, um sein passwort zu änderen#
            db.session.commit()           
            return redirect(url_for('auth.pass_change'))
        else:
            flash('Der Code ist Falsch', category='error')
            return redirect(url_for('auth.codeChecking'))
    

@auth.route('/pass_change' ,methods=['GET', 'POST']) 
def  pass_change(): 
      
    email = session.get('email')
    email = User.query.filter_by(email=email).first()  
    
    if not email or email.code_pass != 'allowed'  :
        return redirect(url_for('auth.email_suchen'))
    else:
        
        form = passChange_Form()
        if request.method == 'GET':
            return render_template('/auth/pass_change.html', 
                                title='code',
                                user=current_user,
                                form = form)
            
        new_pass = request.form.get('new_pass')
        confirm_pass = request.form.get('confirm_pass')
    
        email = session.get('email')
        
        email = User.query.filter_by(email=email).first()
        
                
        if new_pass == confirm_pass:
            email.password = generate_password_hash(password=confirm_pass,method='pbkdf2:sha256') 
            email.code_pass = '' 
            db.session.commit()
            session['email'] = ''
            flash('Ihr Passwort wurde geändert')
            return redirect(url_for('auth.login'))
        else:
            flash('Passwörter stimmen nicht überein', category='error')
            return redirect(url_for('auth.pass_change'))

        
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('erfolgreich abmelden', category='success')
    return redirect(url_for('home.h0me'))
   
