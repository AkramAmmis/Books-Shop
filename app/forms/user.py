from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,EmailField, DateField,SelectField, FileField
from wtforms.validators import email, DataRequired, length,equal_to

class Register_Form(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired(), length(min=4)])
    email = EmailField('Email', validators=[DataRequired()])
    address = StringField('Adresse', validators=[DataRequired()])
    DateOFbirth = DateField('Geburtsdatum', validators=[DataRequired()])
    language = SelectField('Sprache', choices=('Arabic', 'Deutsch', 'Englich'))
    logo = FileField('Logo')
    password = PasswordField('Passwort', validators=[DataRequired(), length(min=6,max=16)])
    confirm = PasswordField('Passwort erneut', validators=[DataRequired(), equal_to('password'), length(min=6,max=16)])
    submit = SubmitField('register')
    
    
class Anmeldung_Form(FlaskForm):
    username = StringField(label='Name oder Email', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired(), length(min=6, max=16)])
    submit = SubmitField('anmelden')
    
    
    
class edit_form(FlaskForm):
    username = StringField('username', validators=[length(min=4, max=12)])
    email = EmailField('email', validators=[length(min=8)])
    password = PasswordField('Password', validators=[length(min=8, max=16)])
    DateOFbirth = DateField('Date of Birth', validators=[])
    language = SelectField('Lanuage', choices=(None,'Arabic', 'Deutsch', 'englich'))
    logo = FileField('Logo')
    old_password = PasswordField('Old Password', validators=[length(min=8, max=16)])
    submit = SubmitField('Save')
    
    
class EmailSuchen_Form(FlaskForm):
     email = EmailField('Email', validators=[DataRequired()])
     submit = SubmitField('suchen')
     
     
class codeChecking_form(FlaskForm):
    code = PasswordField('geben Sie den Code ein : ', validators=[DataRequired(), length(min=4, max=4)])
    submit = SubmitField('eingeben')
    
class passChange_Form(FlaskForm):
    old_pass= PasswordField('Altes Passwort : ', validators=[DataRequired(), length(min=6, max=16)])
    new_pass  = PasswordField('Neus Passwort : ', validators=[DataRequired(), length(min=6, max=16)])
    confirm_pass= PasswordField('Passwort bestätigen: ', validators=[DataRequired(), length(min=6, max=16)])
    submit = SubmitField('OK')