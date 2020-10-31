from flask import Blueprint, jsonify , request
from models.image import Image
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from instagram_web.util.helpers import upload_file_to_s3
from models.imagelike import ImageLike
from models.imagecomment import ImageComment


images_api_blueprint = Blueprint('images_api',
                                 __name__,
                                 template_folder="templates")


@images_api_blueprint.route('')
def showuserimage():
    id=request.args.get("userId")

    user = User.get_by_id((id))
    data = []
    for element in user.images:
        data.append({
            "id": element.id,
            "url": element.full_image_url
        })

    return jsonify(data)


@images_api_blueprint.route('/me')
@jwt_required
def showme():

    user = User.get_or_none(User.username == get_jwt_identity())
    data = []
    for image in user.images:
        data.append(image.full_image_url)

    return jsonify(data)


@images_api_blueprint.route('/', methods=["POST"])
@jwt_required
def create():
    imagefile = request.files.get('image')

    if imagefile == None:
        data = {
            "message": "No image provided",
            "status": "failed"
        }

        return jsonify(data), 400

    image_path = upload_file_to_s3(imagefile, get_jwt_identity())

    user = User.get_or_none(User.username == get_jwt_identity())

    image = Image(user=user, images_pathway=image_path)
    if image.save():
        data = {
            "image_url": image.full_image_url,
            "success": True
        }
        return jsonify(data)


@images_api_blueprint.route('/<id>/toggle_like' , methods=["POST"])
@jwt_required
def imagelike(id):
    print("S:LDKFJSLDFJLSDJFKDF")

    user = User.get_or_none(User.username == get_jwt_identity())

    imagelike = ImageLike.get_or_none(ImageLike.image==id,ImageLike.liker==user)

    if imagelike:
        imagelike.delete_instance()
        data = {
            "image_id": id,
            "liked": False
        }

        return jsonify(data)

    else:
        createimagelike = ImageLike(image=id, liker=user)

        createimagelike.save()
        data = {
            "image_id": id,
            "liked": True
        }

        return jsonify(data)


@images_api_blueprint.route('/<id>/comments')
def imagecomment(id):
    print("XOXOXOXOXOXOXOXOXO")
    image=Image.get_by_id(int(id))
    data=[]
    for element in image.comments:
        data.append({
            "content":element.comment,
            "created_at":element.created_at,
            "id":element.id,
            "posted_by":{
                "email":element.commentator.email,
                "id":element.commentator.id,
                "profileImage":element.commentator.full_image_path,
                "username":element.commentator.username
            }

        })

    return jsonify(data)

@images_api_blueprint.route('/<id>/comments' , methods=["POST"])
@jwt_required
def createcomment(id):
    
    commentator=User.get_or_none(User.username==get_jwt_identity())
    comment=request.json.get("content")

    if comment==None:
        data={
            "message":"Comment content not provided",
            "status":"failed"
        }
        return jsonify(data)

    imagecomment=ImageComment(image=id,commentator=commentator,comment=comment)


    if imagecomment.save():
        data={
            "id":id,
            "status":"success"
        }

        return jsonify(data)

@images_api_blueprint.route('/<id>/likes')
def imagedetail(id):
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")

    image=Image.get_by_id(id)

    likes=[]
    
    for element in image.likes:
        likes.append({
            "email":element.liker.email,
            "id":element.liker.id,
            "profileImage":element.liker.full_image_path,
            "username":element.liker.username
        })

    data={
        "id":id,
        "likes":likes,
        "url":image.full_image_url,
        "owner":{
            "userid":image.user.id,
            "profileImage":image.user.full_image_path,
            "username":image.user.username
        }
    }

    return jsonify(data)







        






