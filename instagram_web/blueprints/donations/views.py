from flask import Blueprint , request, redirect,render_template,url_for , flash
from flask_login import current_user
from instagram_web.util.helpers import gateway
from models.image import Image
from models.user import User
from models.donation import Donation
import stripe
import os
import requests





donations_blueprint=Blueprint("donations",
                                __name__,
                                template_folder="templates")



@donations_blueprint.route('/new')
def new(image_id):
    print(image_id)
    client_token=gateway.client_token.generate()
    image=Image.get_by_id(int(image_id))


    return render_template('donations/new.html' , image=image ,client_token=client_token)


@donations_blueprint.route('/' , methods=["POST"])
def create(image_id):
    payload_nonce=request.form.get("payload_nonce")
    payment_amount=request.form.get("payment_amount")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(payload_nonce)
    
    image=Image.get_by_id(int(image_id))
    user=User.get_by_id(current_user.id)


    result = gateway.transaction.sale({
    "amount": payment_amount,
    "payment_method_nonce": payload_nonce,
    "device_data": None,
    "options": {
      "submit_for_settlement": True
    }
})
    if result.is_success:
        donation=Donation(amount=int(payment_amount), donor=user, image=image)
        donation.save()
        flash(f"Thanks you for the RM{payment_amount} donation {current_user.username}" , "success")
        def send_simple_message():
            	return requests.post(
		                "https://api.mailgun.net/v3/sandboxeaa30d1922044857bee3122cfe3ac0f9.mailgun.org/messages",
		                auth=("api", "0c755bb89badb4492f69d8f73b0cfaac-07e45e2a-8f242430"),
		                data={"from": "Excited User <mailgun@sandboxeaa30d1922044857bee3122cfe3ac0f9.mailgun.org>",
			            "to": ["weikhang_93@hotmail.com"],
			            "subject": "Hello hahaha",
			            "text": "changing the textailgun awesomness!",
                        "html":f"<img src={image.full_image_url}> "})


        print(send_simple_message())



    return redirect(url_for('images.show', image_id=image.id))


@donations_blueprint.route('/stripe' , methods=["POST"])
def stripenew(image_id):
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    stripe.api_key=os.environ.get("STRIPE_API_KEY")
    try:

        checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': 2000,
                            'product_data': {
                                'name': 'Stubborn Attachments',
                                'images': ['https://i.imgur.com/EHyR2nP.png'],
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=f'https://localhost:5000/images/{image_id}/donations' + '/success.html',
                cancel_url=f'https://localhost:5000/images/{image_id}/donations' + '/cancel.html',
            )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403


@donations_blueprint.route("/success.html")
def success(image_id):

    return render_template('donations/success.html')

@donations_blueprint.route("/cancel.html")
def cancel(image_id):

    return render_template('donations/cancel.html')


@donations_blueprint.route('/checkout')
def checkout(image_id):
    image=Image.get_by_id(int(image_id))

    return render_template('donations/checkout.html' , image=image)


@donations_blueprint.route('/testing')
def testing(image_id):
    stripe.api_key = 'sk_test_51HZvbqHyiZLRnqzJOLZZWOtFBAUiUuhzc4PpnGFbSsHXl3qgtF9AWMfENlstDaDL96LwZNgAhX5yIBjERvtFiyNA00DhvRazOn'

    result=stripe.PaymentIntent.create(
    amount=1000,
    currency='myr',
    payment_method_types=['card'],
    receipt_email='jenny.rosen@example.com',
    )

    print(result)
    

    return "stripesssss"