""" User routes """
from flask import Blueprint, session, url_for, redirect, render_template, g
from cloudcourseproject.src.auth import secure

user = Blueprint("user", "user", url_prefix="/user")

@user.route("/logout", methods=["GET"])
def logout():
    """ Log user out """
    session.clear()
    return redirect("/")

@user.route("/profile", methods=["GET"])
@secure("User", False)
def profile():
    """ Serve user page """
    return render_template("/user/profile.jinja", is_authorized=True, user=g.current_user)

def change_user():
    """ Change user password """
    pass

def forgot_password():
    """ Retrieve password if forgot """
    pass