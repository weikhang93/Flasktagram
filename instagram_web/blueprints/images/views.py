from flask import Blueprint , request, render_template,url_for ,redirect , send_file , jsonify , Response ,make_response ,flash
from models.image import Image
from models.user import User
from instagram_web.util.helpers import upload_file_to_s3
from flask_login import login_required, current_user
import io





images_blueprint=Blueprint("images",
                __name__,
                template_folder="templates")


@images_blueprint.route('/', methods=["POST"])
@login_required
def create():
    file=request.files.get("images")

    image_path=upload_file_to_s3(file,current_user.username)
    user=User.get(User.username==current_user.username)


    image=Image(user=user , images_pathway=image_path)

    if image.save():
        flash('You have successfully upload a new image!' , 'success')
    print(file.mimetype)
    # return "hehehe"
    # sendfile()

    # image_binary = read_image(file)

    # response = make_response(image_binary)
    # response.headers.set('Content-Type', 'image/jpeg')
    # response.headers.set(
    #     'Content-Disposition', 'attachment', filename='%s.jpg' % pid)
    # return response

    # return send_file(io.BytesIO(file.read()),
    #                  attachment_filename=file.filename,
    #                  mimetype='image/jpg')
    # return send_file(file.filename,mimetype=f'{file.mimetype}')

    # return jsonify(file)






    # return Response(file,mimetype="text/jpeg")
    return redirect(url_for('users.edit' , id=user.id))

@images_blueprint.route('/<image_id>')
def show(image_id):
    x=0
    image=Image.get_by_id(int(image_id))

    if len(image.top10)<10:
        x=10-len(image.top10)

    print(x)



    return render_template('images/show.html' , image=image, x=x)
