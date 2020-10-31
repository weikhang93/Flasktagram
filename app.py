import os
import config
from flask import Flask , render_template, jsonify , request
from models.base_model import db
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from models.user import User
import stripe
from flask_jwt_extended import JWTManager



stripe.api_key="sk_test_51Ha1aXLywqixhVu00CYH0m3jOkL5grTm7ydsGdQq6pQZPnlap6n1TIhtR9JPJh4R6ZBWOWnCHpB1ak1vcsynh4sp00Iy8gU5tr"




web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CSRFProtect(app)
jwt=JWTManager(app)

login_manager = LoginManager()
login_manager.init_app(app)


login_manager.login_view = "sessions.login"
login_manager.login_message = "Please login first~"
login_manager.login_message_category = "warning"


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id) # get id from session,then retrieve user object from database with peewee query


@app.before_request
def before_request():
    db.connect()

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc




@app.route('/create-session', methods=['POST'])
@csrf.exempt
def create_checkout_session():
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    
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
            success_url="http://localhost:5000/images/8/donations" + '/success.html',
            cancel_url="http://localhost:5000/images/8/donations" + '/cancel.html',
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403
    return "shit"
    