from flask import Flask, redirect, jsonify, request, url_for, Blueprint, flash, session
from paypalrestsdk import Payment, configure
from app.models import db
from app.models.model import Book, Order
from .. import app
from flask_login import current_user, login_required

payment_blueprint = Blueprint('payment_blueprint', __name__)



@payment_blueprint.route('/payment/<int:id>', methods=['POST', 'GET'])
def payment(id):  # put application's code here
    book = Book.query.filter_by(id=id).first()
    title = book.title
    price = book.price
    seller_id = book.user.id
    quantity = request.form.get('quantity')
    session['book_id'] = str(id)
    session['seller_id'] = str(seller_id)
    session['quantity'] = quantity
    configure({
        "mode": app.config['PAYPAL_MODE'],  # sandbox für Tests, live für den Produktivmodus
        "client_id": app.config['PAYPAL_CLIENT_ID'],
        "client_secret":app.config['PAYPAL_CLIENT_SECRET']
    })

    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": url_for("payment_blueprint.confirm_payment", _external=True),  # URL_für_erfolgreiche_Zahlungen
            "cancel_url":  url_for("payment_blueprint.error", _external=True)   # URL_für_abgebrochene_Zahlungen
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": title,
                    "sku": 123,
                    "price": price,
                    "currency": "EUR",
                    "quantity": quantity,
                }]
            },
            "amount": {
                "total": "{:.2f}".format(float(price) * float(quantity)),
                "currency": "EUR"
            },
            "description": "Kauf eines Buchs"
        }],
  
    })
    
    if payment.create():
        for link in payment.links:
            
            if link.method == 'REDIRECT':
                
                return redirect(link.href)

    else:
        return jsonify({"error": payment.error})


@payment_blueprint.route('/confirm_payment', methods=['POST', 'GET'])
def confirm_payment():
    payment_id = request.args.get("paymentId")
    payer_id = request.args.get("PayerID")
    payment = Payment.find(payment_id)
    
    if payment.execute({"payer_id": payer_id}):
        
        order  = Order.query.filter_by(buyer_id=current_user.id).first()
        if order and not order.delivered:
            if str(order.book_id) == session['book_id'] :
                order.quantity += int(session['quantity'])
            else:
                order = Order(book_id=session['book_id'], buyer_id=current_user.id, buyer_name=current_user.username, buyer_adress=current_user.address, seller_id=session['seller_id'],quantity=session['quantity'])
                db.session.add(order)
        else:
            order = Order(book_id=session['book_id'], buyer_id=current_user.id, buyer_name=current_user.username , buyer_adress=current_user.address,seller_id=session['seller_id'],quantity=session['quantity'])
            db.session.add(order)   
        db.session.commit()

        
        flash('Erfolgreich bezahlt und bestellt', category='success')
        
        return redirect(url_for('home.profil'))
    else:
        flash('Es wurde nicht erfolgreich gezahlt, versuchen Sie nochmal!', category='error')
        return url_for('home.profil')

@payment_blueprint.route('/error', methods=['GET'])
def error():
    return 'error'
