from flask import Blueprint, render_template,request,url_for,redirect, flash
from werkzeug.security import check_password_hash
from models.user import User
from flask_login import login_user , logout_user , login_required , current_user
from instagram_web.util.google_oauth import oauth






sessions_blueprint=Blueprint('sessions',
                            __name__,
                            template_folder="templates")


@sessions_blueprint.route('/new')
def new():

    return render_template('new.html')

@sessions_blueprint.route('/' , methods=["POST"])
def create():
    email=request.form.get("email")
    password=request.form.get("password")

    
    user=User.get_or_none(User.email==email)
    print(current_user.is_authenticated)

    if user:
        if check_password_hash(user.hashed_password,password):
            login_user(user)


            flash(f"You have succesfully logged in! Welcome {user.username}" , "success")

            

            return redirect(url_for('users.feed' , username=current_user.username))

    flash("Please provide a correct email and password!" , 'danger')

    return redirect(url_for('home'))

@sessions_blueprint.route('/<id>/delete' , methods=["POST"])
@login_required
def destroy(id):
    logout_user()
    flash("You have successfully logout. You are welcome back anytime" , "danger")

    return redirect(url_for('home'))



@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route("/authorize/google")
def authorize():
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash(f"You have successfully logged in using your gmail {user.email} ! Welcome onboard {user.username}" , "success")
        return redirect(url_for('home'))
    else:
        return "NO USER FUCKER"


