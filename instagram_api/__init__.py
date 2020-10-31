from app import app,csrf
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from instagram_api.blueprints.users.views import users_api_blueprint
from instagram_api.blueprints.images.views import images_api_blueprint
from instagram_api.blueprints.login.views import login_api_blueprint


csrf.exempt(users_api_blueprint)
csrf.exempt(images_api_blueprint)
csrf.exempt(login_api_blueprint)


app.register_blueprint(users_api_blueprint, url_prefix='/api/users')


app.register_blueprint(images_api_blueprint, url_prefix="/api/images")


app.register_blueprint(login_api_blueprint,url_prefix="/api/login")
