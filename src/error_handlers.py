""" Routes to handle application errors """
from flask import render_template, url_for, redirect
from cloudcourseproject.src.auth import AuthorizationError
from cloudcourseproject.src.app import app

@app.errorhandler(AuthorizationError)
def handle_gremlin_server_error(exception):
    """ Bad request error handler """
    return redirect(url_for("authorization.login", error=str(exception)))

@app.errorhandler(404)
def handle_not_found(exception):
    """ Route not found error handler """
    return render_template("404.jinja")
