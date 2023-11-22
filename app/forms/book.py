from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,DateField,SelectField, FileField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, length,equal_to

class AddBook_form(FlaskForm):
    id = IntegerField('id_book')
    title = StringField('Title', validators=[DataRequired(), length(min=4)])
    description = StringField('Description', validators=[DataRequired(), length(min=4)])
    price = IntegerField('Price', validators=[DataRequired()])
    url_img = StringField('Image Url')
    image = FileField('oder Image hochladen')
    submit = SubmitField('veröffentlichen')
    
class EditBook_form(FlaskForm):
    id = IntegerField('id_book')
    title = StringField('Title', validators=[DataRequired(), length(min=4)])
    description = StringField('Description', validators=[DataRequired(), length(min=4)])
    price = IntegerField('Price', validators=[DataRequired()])
    url_img = StringField('Image Url')
    image = FileField('Image')
    submit = SubmitField('Ok')
    