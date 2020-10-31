from flask import Blueprint, request, jsonify
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from instagram_web.util.helpers import upload_file_to_s3


users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])
def index():

    users = User.select()
    data = []

    for user in users:
        data.append({"username": user.username,
                     "id": user.id,
                     "email": user.email,
                     "profileImage": user.full_image_path})

    return jsonify(data)


@users_api_blueprint.route('/<id>')
def show(id):

    user = User.get_or_none(User.id == id)

    if user:
        data = {
            "id": user.id,
            "profileImage": user.full_image_path,
            "username": user.username
        }

        return jsonify(data)
    else:
        data = {
            "message": "User does not exist",
            "status": "failed"
        }
        return jsonify(data), 404


@users_api_blueprint.route('/me')
@jwt_required
def showme():
    user = User.get_or_none(User.username == get_jwt_identity())

    data = {
        "email": user.email,
        "id": user.id,
        "profile_picture": user.full_image_path,
        "username": user.username
    }

    return jsonify(data)


@users_api_blueprint.route('/check_name')
def checkname():
    username = request.args.get("username")

    user = User.get_or_none(User.username == username)
    if user:
        data = {
            "exist": True,
            "valid": False
        }
        return jsonify(data)

    else:
        data = {
            "exist": False,
            "valid": True
        }
        return jsonify(data)


@users_api_blueprint.route('/', methods=["POST"])
def create():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(username)

    if username == None or email == None or password == None:
        data = {
            "message": ["All fields are required"],
            "status": "failed"
        }
        return jsonify(data), 400

    user = User.get_or_none(User.username == username)
    if user:
        data = {"status": "fail"}
        message = ["Username is already in use"]
        if email == user.email:
            message.append("Email is already in use")

        data["message"] = message

        return jsonify(data), 400

    user2 = User.get_or_none(User.email == email)
    if user2:
        data = {"status": "fail"}
        message = ["Email is already in use"]   
        if username == user2.username:
            message.append("Username is already in use")

        data["message"] = message

        return jsonify(data), 400

    user3 = User(username=username, email=email,
                 hashed_password=generate_password_hash(password))

    if user3.save():
        data = {
            "message": "Successfully created a user",
            "status": "success",
            "user": {
                "id": user3.id,
                "profile_picture": user3.full_image_path,
                "username": user3.username
            }
        }
        return jsonify(data), 201

@users_api_blueprint.route('/profileImage' , methods=["POST"])
@jwt_required
def profileimage():
    user=User.get_or_none(User.username==get_jwt_identity())
    profileImage= request.files.get("profileImage")


    image_path=upload_file_to_s3(profileImage,user.username)
    user.profile_image_pathway=image_path

    if user.save():
        data={
            "id":user.id,
            "profile_picture":user.full_image_path,
            "username":user.username
        }

        return jsonify(data)


    
    



