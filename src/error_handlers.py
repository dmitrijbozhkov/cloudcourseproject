""" Routes to handle application errors """
from cloudcourseproject.src.auth import AuthorizationError
from cloudcourseproject.src.app import app

@app.errorhandler(AuthorizationError)
def handle_gremlin_server_error(exception):
    """ Bad request error handler """
    return "", 500

@app.errorhandler(404)
def handle_not_found(exception):
    """ Route not found error handler """
    return "", 404
