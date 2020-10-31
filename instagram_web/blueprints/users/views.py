from flask import Blueprint, render_template, request, url_for, redirect,flash
from werkzeug.security import generate_password_hash , check_password_hash
from werkzeug import secure_filename
from models.user import User
import boto3
import os
from instagram_web.util.helpers import upload_file_to_s3
from models.image import Image
from models.fanidol import FanIdol
from flask_login import current_user,login_required




users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():

    return render_template('users/new.html') 


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get("username")
    # request.form.get('csrf_token')
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@XXXXXXXXXXXXXXXXXXXXXXXXXX")
    # print(request.form.get('csrf_token'))
    email = request.form.get("email")
    password = request.form.get("password")
    hashed_password = generate_password_hash(password)
    if username=="" or email=="" or password=="":
        flash("Please provide all the credential needed!" , "danger")
        return redirect(url_for('users.new'))

    checkforusername=User.get_or_none(User.username==username)
    checkforemail=User.get_or_none(User.email==email)

    if checkforusername and checkforemail:
        flash("Username and email are both used, have you registered an account before?","danger")

        return redirect(url_for('users.new'))

    if checkforusername:
        flash("This username is already taken. Please come up with a cooler name!" ,"danger")
        return redirect(url_for('users.new'))

    if checkforemail:
        flash("This email is already used. Please use another email" , 'danger')
        return redirect(url_for('users.new'))

    
            
    

    new_user = User(username=username, email=email,
                    hashed_password=hashed_password)

    if new_user.save():
        flash("Your account has been created! Login now!" , "success")

    return redirect(url_for('users.new'))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2")

    user=User.get(User.username==username)

    all_images=Image.select().where(Image.user_id==user.id)
    print(current_user.full_image_path)


 

    user2=User.select().where(User.id==current_user.id)







    return render_template('users/show.html' ,all_images=all_images , user=user)
    


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    


    return render_template('users/edit.html')


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user=User.get_by_id(int(id))
    newusername=request.form.get('username')
    current_password=request.form.get("current_password")
    new_password=request.form.get("new_password")

    if user.username==newusername and current_password=="" and new_password=="":
        flash("Please provide the correct credential if you want to update your profile detail", "danger")
        return redirect(url_for('users.edit' , id=current_user.id))

    if newusername!=user.username:
        checkforexistingusername=User.get_or_none(User.username==newusername)
        if checkforexistingusername:
            flash('This username has already taken. Please come up with a better one!','danger')

            return redirect(url_for('users.edit' , id=current_user.id))



    if current_password=="" and user.username!=newusername:
        checkforexistingusername=User.get_or_none(User.username==newusername)
        if checkforexistingusername:
            flash('This username has already taken. Please come up with a better one!','danger')
            return redirect(url_for('users.edit',id=current_user.id))
        else:
            user.username=newusername
            if user.save():
                flash('Username is updated!' ,'success')
                return redirect(url_for('users.edit' , id=current_user.id))


     


        
        
    
    if user.username==newusername:
        if check_password_hash(user.hashed_password,current_password):
            user.hashed_password=generate_password_hash(new_password)
            if user.save():
                flash("Password is updated!" , 'success')
                
                return redirect(url_for('users.edit' , id=current_user.id))






    user.username=newusername
    if check_password_hash(user.hashed_password,current_password):
        user.hashed_password=generate_password_hash(new_password)
        if user.save():

            flash("Username and password is updated!" , 'success')

            return redirect(url_for('users.edit' , id=current_user.id))




    else:
        flash("Wrong Password, please make sure you key in the correct password." , "danger")
        return redirect(url_for('users.edit' , id=current_user.id))


    


    

    



@users_blueprint.route('/<id>/profile_image', methods=["POST"])
def upload_profile_image(id):

    
    user=User.get_by_id(int(id))
    file=request.files.get("profile_image")

    file.filename = secure_filename(file.filename)

    image_path=upload_file_to_s3(file,user.username)

    user.profile_image_pathway=image_path

    if user.save():
        flash("Profile Image updated!" , "success")




    return redirect(url_for('users.edit' ,id=id))


@users_blueprint.route('/<user_id>/private/edit' , methods=["POST"])
def private(user_id):

    shit=request.form.get("public")

    print(shit)
    user=User.get_by_id(current_user.id)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    if shit==None:
        print(user.is_private)
        flash("You account is public now! Everyone can see your images." , "success")
        user.is_private=False
        print(user.is_private)
        print(current_user.is_private)
    else:
        flash("Your account is private now! Only approved fan can see your images." , 'success')
        user.is_private=True
    

    user.save()

    return redirect(url_for('users.edit' , id=user.id))

@users_blueprint.route('/<id>/follow' , methods=["POST"])
def follow(id):
    fan=User.get_by_id(current_user.id)

    fan.follow(int(id))
    idol=User.get_by_id(int(id))

    return redirect(url_for('users.show' , username=idol.username))


@users_blueprint.route('/unfollow/<idol_id>' , methods=["POST"])
def unfollow(idol_id):

    current_user.unfollow(int(idol_id))

    user=User.get_by_id(int(idol_id))





    return redirect(url_for('users.show',username=user.username))




# @users_blueprint.route('/<username>/follow')
# def my_idols(username):

#     #test using current_user
#     user=User.get_by_id(current_user.id)
#     print("$@#$@#$@#$@#$@#$@#$@#$@#$@#$@#$@$@#$")






#     return render_template('/users/my_idol.html', user=user)



@users_blueprint.route('/<username>/pending_idols')
def pending_idols(username):



    




    return render_template('users/pending_idols.html')




@users_blueprint.route('/<username>/my_idols')
def my_idols(username):


    return render_template('users/my_idols.html')






@users_blueprint.route('/<fan_username>/approve' , methods=["POST"])
def approve(fan_username):
    fan=User.get_or_none(User.username==fan_username)

    
    inputbutton=request.form.get("inputbutton")
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxdxx")
    print(inputbutton)
    
    
    if inputbutton=="approve":
        fanidol=FanIdol.get_or_none(FanIdol.fan==fan)
        fanidol.approved=True
        fanidol.save()



        



    else:   
        
        print(fan.username)

        fanidol=FanIdol.get_or_none(FanIdol.fan==fan)
        print("XOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXO")
        fanidol.blocked=True
        fanidol.save()

        return redirect(url_for('users.blockeduser'))
        

    # current_user.approve(fan.id)
    # print("333333333333333333333333333333333333333333333333333333333333333333")


    return redirect(url_for('users.fan_requests' , username=current_user.username))


@users_blueprint.route('/<username>/fan_requests')
def fan_requests(username):


    return render_template('users/fan_requests.html')

@users_blueprint.route('/<username>/my_fans')
def my_fans(username):



    return render_template('users/my_fans.html')




@users_blueprint.route('/<username>/feed')
@login_required
def feed(username):




    return render_template('users/feed.html')




@users_blueprint.route('/search' , methods=["POST"])
def search():
    print("@@@@@@@@@@@@@LJDLFKJSKJDFKSDJF:KSJDFKJDSF:KDSF")
    username=request.form.get("username")
    print(username)

    search_result=current_user.search_result(username)




    return render_template('users/search.html' , search_result=search_result , username=username)


@users_blueprint.route('/blocked')
def blockeduser():

    # print("FLKSFKLSJDLKF:J:LKGJ:LSKDJFLKSJDFL:KJSDLGK:JSLDK:FJLKSDJFLKSJDF:LKSDJFLKSJDF:DKJLDFKSDKFJ")
    return render_template('users/blocked.html')


@users_blueprint.route('/unblock/<fan_username>' , methods=["POST"])
def unblock(fan_username):
    fan=User.get_or_none(User.username==fan_username)
    fanidolrow=FanIdol.get_or_none(FanIdol.idol==current_user.id,FanIdol.fan==fan.id)

    fanidolrow.blocked=False
    fanidolrow.save()






    return redirect(url_for('users.blockeduser'))
