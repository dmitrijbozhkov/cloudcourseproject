""" Authorization routes """
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask import Blueprint, g, Response, request
from cloudcourseproject.src.celery import celery
from cloudcourseproject.src.auth import secure

authorization = Blueprint("authorization", "authorization", url_prefix="/authorization")

@authorization.route("/login", methods=["GET", "POST"])
def login():
    """ Do stuff on login """
    print(celery)
    return ("", 200)
