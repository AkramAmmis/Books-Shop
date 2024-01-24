from flask import redirect,render_template,Blueprint,request,flash,url_for, session
from flask_login import current_user, login_required
import validators
from ..models.model import Book,db, CartItem, Order, User
from  app.forms.book import AddBook_form,EditBook_form
from app.forms.user import edit_form
from os import rename, path
from werkzeug.utils import secure_filename
import requests,imghdr
from PIL import Image
from werkzeug.security import generate_password_hash, check_password_hash
from .email_confirm import token, check_token
import os.path
home = Blueprint('home', __name__)

@home.route('/')
def h0me():
    books = Book.query.all()
    return render_template('home/index.html',title='Page',user=current_user, books=books)

@home.route('/profil')
@login_required
def profil():
    books = Book.query.all()
    orders = Order.query.all()
    
    book = Book.query.filter_by(id=current_user.id).first()
    if not book:
        orders_sum = None
    else:
    
        orders_sum = 0
        for order in orders:
            if order.seller_id == current_user.id:
                orders_sum += 1
    return render_template('home/profil.html',title='Page', user=current_user, books=books, orders=orders_sum)

@home.route('/bookdetails/<int:id>')
def bookdetails(id):
    book = Book.query.filter_by(id=id).first()
    books = Book.query.all()
    return render_template('home/book_details.html',title='bookdetails',user=current_user, book=book, books=books)

@home.route('/warenkorb')
@login_required
def warenkorb():
    books = Book.query.all()
    cartitems = current_user.cartitems 
    prices = []
    for cartitem in cartitems:
        for book in books:
            if book.id == cartitem.book_id : 
                prices.append(book.price)
    summe = sum(prices)
    return render_template('home/warenkorb.html', title='Warenkorb',user=current_user , books=books, gesamtsumme=summe)

@home.route('/add_to_shopping_carts/<int:id>')
@login_required
def add_to_shopping_carts(id):
    book = Book.query.filter_by(id=id).first()
    new_cartitem = CartItem(user_id=current_user.id, book_id=id,author=current_user.id)
    print(current_user)
    print(current_user.id)
    book.warenkorb = 1
    db.session.add(new_cartitem)
    db.session.commit()
    return redirect(request.referrer)

@home.route('/remove_from_cart/<int:id>')
@login_required
def remove_from_cart(id):
    book = Book.query.filter_by(id=id).first()
    cartitem = CartItem.query.filter_by(book_id=id,user_id=current_user.id).first()
    book.warenkorb = 0
    db.session.delete(cartitem)
    db.session.commit()
        
    return redirect(request.referrer)

@home.route('/new_book')
@login_required
def new_book():
    form = AddBook_form()
    return render_template('home/new_book.html',user=current_user, form=form)

@home.route('/add_book', methods=['POST'])
@login_required
def add_book():
    form = AddBook_form()
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')
    url_img = request.form.get('url_img')
    image = form.image.data 


            
    if url_img:
         #überprüfen, ob die URL gültig ist
            if validators.url(url_img) :
                #überprüfen, ob die URL zu einem Bild Führt
                response = requests.get(url_img)
                type = response.headers.get('Content-Type')
                                                        
                if type.startswith('image') == True:

                        new_book = Book(title=title, price=price,description=description,image=url_img, author=current_user.id)
                        db.session.add(new_book)
                        db.session.commit()
                        flash('Es wurde hinzufügt', category='success')
                else :
                    flash(category='error', message='Die eingegebene Image-URL ist ungültig')
            else :
                flash(category='error', message='Die eingegebene Image-URL ist ungültig')
                
    elif image:
        if imghdr.what(image) != None: #überprüfen, ob die Datei ein bild ist
            image_name = form.image.data.filename
            file_name = secure_filename(image_name)
            image.save('app/static/book_images/' + file_name)
            name_save = title.replace(" ", "") + '.jpg' 
            rename('app/static/book_images/' + file_name, 'app/static/book_images/' + name_save)
            new_book = Book(title=title, price=price,description=description,image=url_img,image_name=name_save, author=current_user.id)
            db.session.add(new_book)
            db.session.commit()
            flash('Es wurde hinzufügt', category='success')
        else:
            flash('Die image ist ungültig', category='error')
         
         

    
    return redirect(request.referrer)

@home.route('/del_book/<int:id>')
@login_required
def del_book(id):
    book = Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    flash('Es wurde gelöschet', category='success')
    return redirect(url_for('home.profil'))


@home.route('/edit_book_page/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_book(id):
    form = EditBook_form()
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')
    url_img = request.form.get('url_img')
    image = form.image.data
    change = False
    book = Book.query.filter_by(id=id).first()
    
    if request.method == 'POST':
        
        if title and title != book.title :
            book.title = title
            change = True
            
        if description and description != book.description :
            book.description = description
            change = True

        if int(price) != book.price :
            print(price)
            print(book.price)
            book.price = price
            change = True

        if url_img and url_img != book.image :
            if validators.url(url_img):
                #überprüfen, ob die URL zu einem Bild Führt
                response = requests.get(url_img)
                type = response.headers.get('Content-Type')
                                                        
                if type.startswith('image') == True:
                        book.image = url_img
                        change = True
                else :
                    flash(category='error', message='Die eingegebene Image-URL ist ungültig')
            else :
                flash(category='error', message='Die eingegebene Image-URL ist ungültig')
        elif image:
            if imghdr.what(image) != None: #überprüfen, ob die Datei ein bild ist
                image_name = form.image.data.filename
                file_name = secure_filename(image_name)
                image.save('app/static/book_images/' + file_name)
                name_save = title.replace(" ", "") + '.jpg' 
                rename('app/static/book_images/' + file_name, 'app/static/book_images/' + name_save)
                book.image_name = name_save
                change = True
     
        if change == True:
            db.session.commit()
            flash(category='success', message=' die Änderung wurde gespeichert')
        else:
            flash(category='success', message=' es wurde nichts geändert')
            
            
        return redirect(f'/bookdetails/{book.id}')
    
    return render_template('home/book_edit.html', user=current_user, form=form, book=book)

@home.route('/order_details/<int:id>')
@login_required
def order_details(id):
    book = Book.query.filter_by(id=id).first()
    return render_template('home/order_details.html', user=current_user, book=book)


@home.route('/kauforders', methods=['POST', 'GET'])
@login_required
def kauforders():
    books = Book.query.all()
    orders = Order.query.all()
    return render_template('home/kauforders.html', user=current_user, books=books,orders=orders)

@home.route('/kauforders/delivered/<int:id>', methods=['POST', 'GET'])
@login_required
def delivered(id):
    order = Order.query.filter_by(id=id).first()
    order.delivered = True
    db.session.commit()
    return redirect(url_for('home.kauforders'))

@home.route('/kauforders/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def delete(id):
    order = Order.query.filter_by(id=id).first()
    if order.seller_id == current_user.id :
        order.seller_id = 0
    elif order.buyer_id == current_user.id :
        order.buyer_id = 0
        
    if order.buyer_id == 0 and order.seller_id == 0:
        db.session.delete(order)
    
    db.session.commit()
    flash('Es wurde erfolgreich gelöscht')
    return redirect(request.referrer)



@home.route('/orders', methods=['POST', 'GET'])
@login_required
def orders():
    books = Book.query.all()
    orders = Order.query.all()
    return render_template('home/orders.html', user=current_user, books=books,orders=orders)


   
@home.route('/user_data')
@login_required
def user_data():

    return render_template('home/user_data.html', 
                                user=current_user,
                                title='User Data')
    
    
       
@home.route('/user_data_edit', methods=['POST', 'GET'])
@login_required
def user_data_edit():
    form = edit_form()
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    DateOFbirth = request.form.get('DateOFbirth')
    language = request.form.get('language')
    logo = form.logo.data
    old_password= request.form.get('old_password')
    print(current_user.language,'#######')
    print(logo)
    print(DateOFbirth)
    user = User.query.filter_by(username=current_user.username).first()
    print(current_user.DateOFbirth)
    def check_password():
        if old_password:
            if check_password_hash(user.password, old_password):
                return 1
            else:
                return 0
        else:
            return 2 # muss man ein passwort eingeben

    if request.method == 'POST':
        if (username != current_user.username or email != current_user.email  or password or DateOFbirth != current_user.DateOFbirth
            or (current_user.language != language and language != 'None') or logo):
            if check_password() == True :

            ################# Username Edit ###############
                if username != current_user.username:
                    if not User.query.filter_by(username=username).first(): 
                        user.username=username
                        db.session.commit()
                        flash('new name is saved', category='success')
                    else:
                        flash('Username is already in use. ', category='error')

            ################# Email Edit ##################
            
                if email != current_user.email:
                    if not User.query.filter_by(email=email).first():
                        #new_data['new_email']=email
                        session['new_email']= email
                        email = email
                        print(email)
                        
                        token(email,'home')
                        flash('Pless Check your MailBox.', category='success')
                    else:
                       flash('email is already in use. ', category='error')

            ################# Password Edit ################## 
                if password :
                    if not check_password_hash(current_user.password, password):
                        current_user.password = generate_password_hash(password, method='pbkdf2:sha256')
                        db.session.commit()
                        flash('new pass is saved', category='success')
                    else:
                        flash('this pass is alredy in use!', category='success')
            ############## Date of birth Edit ################
                if DateOFbirth != str(current_user.DateOFbirth) :
                    current_user.DateOFbirth = DateOFbirth
                    db.session.commit()
                    flash('datum ist gespeichert',category='success')
            ############## language Edit #####################
                if current_user.language != language and language != 'None':
                    current_user.language = language
                    db.session.commit()
                    flash('neue sprache ist gespeichert',category='success')
            ################ logo Edit ######################
                if logo:
                    logo_name = form.logo.data.filename
                    file_name = secure_filename(logo_name)
                    if not os.path.exists('app/static/user_logo'):
                        os.mkdir('app/static/user_logo')
                    logo.save('app/static/user_logo/' + file_name)
                    name_save = username.replace(" ", "") + '.jpg' 
                    
                    
                    rename('app/static/user_logo/' + file_name, 'app/static/user_logo/' + name_save)
                    current_user.logo_name = name_save
                    db.session.commit()
                    flash('logo ist gespeichert',category='success')
            #################################################
            elif check_password() == 2:
                flash('enter old pass',category='error')       
            else:
                flash('password error', category='error') 
        else:
            flash('nothing to change','erorr')


    return render_template('home/UserData_edit.html',
    user = current_user,
    form=form,
    logo= current_user.logo_name)
 
   
   
@home.route('/edit/check_token/<token>', methods=['POST', 'GET'])
def confirm(token):
    if check_token(token, False) :
      current_user.email = session['new_email'] 
      db.session.commit()
      flash('neus email ist gespeichert')
    else:
        flash('URL ist nicht mehr gültig', category='error')
    return redirect(url_for('home.user_data'))