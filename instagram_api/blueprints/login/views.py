from flask import Blueprint, request , jsonify
from models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash


login_api_blueprint = Blueprint('login_api',
                                __name__,
                                template_folder="templates")


@login_api_blueprint.route('/' , methods=["POST"])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@XXXXXXXXXXXXXXXXXXXXXX")
    print(username)
    print(password)

    user = User.get_or_none(User.username == username)

    if user:
        if check_password_hash(user.hashed_password, password):
            data = {
                "auth_token": create_access_token(identity=user.username),
                "message": "Successfully signed in",
                "status": "success",
                "user": {
                    "id": user.id,
                    "profile_picture": user.full_image_path,
                    "username": user.username
                }
            }

            return jsonify(data), 201

        else:
            data = {
                "message": "Wrong password",
                "status": "fail"
            }

            return jsonify(data) ,401
        
    else:
        data={
            "message":"Sorry , There is no such username in our application.",
            "status":"failed"

        }
        return jsonify(data) , 401
