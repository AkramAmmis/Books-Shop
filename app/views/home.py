from flask import redirect,render_template,Blueprint,request,flash,url_for
from flask_login import current_user, login_required
import validators
from ..models.model import Book,db, CartItem, Order
from  app.forms.book import AddBook_form,EditBook_form
from os import rename
from werkzeug.utils import secure_filename
import requests,imghdr
from PIL import Image

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
        if imghdr.what(image) != None: # überprüfen, ob die Datei ein bild ist
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
            if validators.url(url_img) :
                #überprüfen, ob die URL zu einem Bild Führt
                response = requests.get(url_img)
                type = response.headers.get('Content-Type')
                                                        
                if type.startswith('image') == True:
                        book.image = url_img
                        db.session.commit()
                        flash('Es wurde hinzufügt', category='success')
                else :
                    flash(category='error', message='Die eingegebene Image-URL ist ungültig')
            else :
                flash(category='error', message='Die eingegebene Image-URL ist ungültig')
     
        if change == True:
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
