from flask import Flask, redirect, jsonify, request, url_for, Blueprint, flash
from paypalrestsdk import Payment, configure
from app.models import db
from app.models.model import Book
from .. import app
payment_blueprint = Blueprint('payment_blueprint', __name__)



@payment_blueprint.route('/payment/<int:id>', methods=['POST', 'GET'])
def payment(id):  # put application's code here
    book = Book.query.filter_by(id=id).first()
   
    title = book.title
    price = book.price
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
                    "sku": "123",
                    "price": price,
                    "currency": "EUR",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": price,
                "currency": "EUR"
            },
            "description": "Kauf eines Buchs"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.method == 'REDIRECT':
                print('11', redirect(link.href))
                return redirect(link.href)

    else:
        return jsonify({"error": payment.error})


@payment_blueprint.route('/confirm_payment', methods=['POST', 'GET'])
def confirm_payment():
    payment_id = request.args.get("paymentId")
    payer_id = request.args.get("PayerID")
    payment = Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        flash('Es wurde erfolgreich gezahlt', category='success')
        return redirect(url_for('home.profil'))
    else:
        flash('Es wurde nicht erfolgreich gezahlt, versuchen Sie nochmal!', category='error')
        return url_for('home.profil')

@payment_blueprint.route('/error', methods=['GET'])
def error():
    return 'error'
