""" Authorization routes """
from wtforms.validators import ValidationError
from flask import Blueprint, g, request, redirect, render_template, url_for, session
from cloudcourseproject.src.celery import celery
from cloudcourseproject.src.config import config
from cloudcourseproject.src.model import User, Role, db
from cloudcourseproject.src.auth import authorize, NotAuthorizedError, create_token, hash_password
from cloudcourseproject.src.authorization.validators import LoginForm, CreateAccountForm

authorization = Blueprint("authorization", "authorization", url_prefix="/authorization")

@authorization.route("/login", methods=["GET", "POST"])
def login():
    """ Login into account or redirect to google login """
    form = LoginForm()
    if request.method == "GET" or not form.validate_on_submit():
        return render_template("authorization/login.jinja", form=form)
    if request.method == "POST":
        try:
            user = authorize(form.email.data, form.password.data)
            token = create_token(user)
            session[config["SESSION_TOKEN"]] = token
            return redirect(url_for("user.profile"))
        except NotAuthorizedError:
            form.password.errors.append(ValidationError("Email or password are incorrect"))
            return render_template("authorization/login.jinja", form=form)
    raise RuntimeError("Invalid request")

@authorization.route("/create", methods=["GET", "POST"])
def create():
    """ Create new account """
    form = CreateAccountForm()
    if request.method == "GET" or not form.validate_on_submit():
        return render_template("authorization/create.jinja", form=form)
    if request.method == "POST":
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hash_password(form.password.data),
            is_activated=False,
            role=Role.query.filter_by(name="User").first()
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("authorization.login")) # send verification email
    raise RuntimeError("Invalid request")
