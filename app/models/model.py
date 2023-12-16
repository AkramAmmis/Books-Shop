from . import db
from flask_login import UserMixin
from datetime import datetime
from . import ma

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    DateOFbirth = db.Column(db.Date())
    language = db.Column(db.String(255))
    confirm_on = db.Column(db.Boolean(), default=False)
    password = db.Column(db.String(255))
    logo_name = db.Column(db.String(255)) 
    code_pass = db.Column(db.String(255))
    address = db.Column(db.String(255))
    books = db.relationship('Book', backref='user', lazy=True) #many - es ist möglich, dass ein user mehrere bücher hat - (user.books): so werden die Bücher abgefragt, die zu dem User gehören.
    cartitems = db.relationship('CartItem', backref='user', lazy=True) 
    #orders = db.relationship('Order', backref='user', lazy=True) 
    
class Book(db.Model):
        id = db.Column(db.Integer,autoincrement=True, primary_key=True)
        image = db.Column(db.String(255))
        title = db.Column(db.String(255))
        description = db.Column(db.String(1000))
        price = db.Column(db.Integer())
        time = db.Column(db.DateTime(), default=datetime.utcnow())
        warenkorb =  db.Column(db.Boolean(), default=False)
        image_name = db.Column(db.String(255)) 
        author = db.Column(db.Integer, db.ForeignKey(
        'user.id')) #one - jedes buch gehört zu einem user - (book.user): So wird der User abgefragt, dem das Buch gehört.
        #cartitems = db.relationship('CartItem', backref='book', lazy=True)    
        
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id'))
                       

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    book_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer) 
    buyer_id = db.Column(db.Integer) 
    buyer_name = db.Column(db.String(255))
    buyer_adress = db.Column(db.String(255))
    delivered = delivered = db.Column(db.Boolean(), default=False)
    seller_id = db.Column(db.Integer)
    
    
class UserSchema(ma.Schema):
    def Meta():
        fields = ['email']
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)