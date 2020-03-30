""" Authorization API """
import hashlib, binascii, os
from functools import wraps
from datetime import datetime, timedelta
import jwt
from flask import session, g
from cloudcourseproject.src.config import config
from cloudcourseproject.src.model import User, Role

class AuthorizationError(RuntimeError):
    """ Authorization errors class """

class NotAuthorizedError(AuthorizationError):
    """ Authorization failed """

class NotEnoughPriveleges(AuthorizationError):
    """ User has not enough priveleges to access the resource """

class InvalidTokenError(AuthorizationError):
    """ Error in token structure """

class TokenExpired(AuthorizationError):
    """ Token is expired """

ALGORITHM = "HS256"

def create_token(user):
    """ Get user and create a token for him """
    return jwt.encode(
        {
            "user_id": user.user_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=config["JWT_ACCESS_TOKEN_EXPIRES"])
        },
        config["JWT_SECRET_KEY"],
        algorithm=ALGORITHM
    )

def hash_password(password):
    """ Hash password using salt in Flask """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
    pwdhash = hashlib.pbkdf2_hmac(
        "sha512",
        password.encode("utf-8"),
        salt,
        100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode("ascii")

def verify_password(password, check_password):
    """ Verify stored password against given """
    salt = password[:64]
    stored_password = password[64:]
    pwdhash = hashlib.pbkdf2_hmac(
        "sha512",
        check_password.encode("utf-8"),
        salt.encode("ascii"),
        100000)
    pwdhash = binascii.hexlify(pwdhash).decode("ascii")
    return pwdhash == stored_password

def identify(token):
    """ Check if user exists """
    token_data = None
    try:
        token_data = jwt.decode(token, config["JWT_SECRET_KEY"], algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError as err:
        raise TokenExpired(str(err))
    except jwt.InvalidTokenError as err:
        raise InvalidTokenError(str(err))
    if not token_data.get("user_id"):
        raise InvalidTokenError("Malformed token")
    user = User.query.filter_by(user_id=token_data["user_id"]).first()
    if not user:
        raise NotAuthorizedError("User not found")
    return user

def authorize(email, password):
    """ Authorize user into account """
    user = User.query.filter_by(email=email).first()
    if not user:
        raise NotAuthorizedError("User not found")
    if verify_password(user.password, password):
        return user
    raise NotAuthorizedError("Wrong password")

def _validate_user(token, role_rank, activated):
    """ Gets user and validates him """
    user = identify(token)
    if not user:
        raise NotAuthorizedError(f"User not found")
    if user.role.rank < role_rank:
        raise NotEnoughPriveleges("You can't access this resource, please contact admin")
    if user.is_activated or activated:
        return user
    raise NotEnoughPriveleges("User should be authorized to access the resource")

def secure(role: str, acivated=True):
    """ Modify route so that it can be accessed only by users with high enough role rank """
    rank = config["roles"].index(role)
    def check_role(route):
        @wraps(route)
        def intermediate(*args, **kwargs):
            token = session.get(config["SESSION_TOKEN"])
            if not token:
                raise NotAuthorizedError("Please authorize yourself")
            user = _validate_user(token, rank, acivated)
            g.current_user = user
            return route(*args, **kwargs)
        return intermediate
    return check_role
