""" Test authentication functionality """
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock, mock_open, call
import pytest
import jwt
from cloudcourseproject.src.config import config
from cloudcourseproject.src.auth import (
    create_token,
    _validate_user,
    secure,
    identify,
    ALGORITHM,
    InvalidTokenError,
    TokenExpired,
    NotAuthorizedError)

@patch("cloudcourseproject.src.model.User")
def test_create_token_should_get_user_model_and_return_token_with_username(user_mock):
    """ create_tocken should create tocken out of model """
    user_mock.user_id = 1
    token = create_token(user_mock)
    decoded_token = jwt.decode(token, config["JWT_SECRET_KEY"], algorithms=[ALGORITHM])
    assert decoded_token["user_id"] == user_mock.user_id

def test_identify_should_raise_error_if_token_has_no_user_id_in_payload():
    """ identify gets token and raises InvalidTokenError if it doesn't fave user_id field"""
    invalid_token = jwt.encode(
        {
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=config["JWT_ACCESS_TOKEN_EXPIRES"])
        },
        config["JWT_SECRET_KEY"],
        algorithm=ALGORITHM
    )
    with pytest.raises(InvalidTokenError) as errorval:
        identify(invalid_token)
    assert isinstance(errorval.value, InvalidTokenError)

def test_identify_should_raise_tokenexpired_if_token_is_expired():
    """ identify should raise TokenExpired if exp is lower, than iat """
    invalid_token = jwt.encode(
        {
            "user_id": 123,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() - timedelta(days=config["JWT_ACCESS_TOKEN_EXPIRES"])
        },
        config["JWT_SECRET_KEY"],
        algorithm=ALGORITHM
    )
    with pytest.raises(TokenExpired) as errorval:
        identify(invalid_token)
    assert isinstance(errorval.value, TokenExpired)

# @
# def test_identify_should_raise_notauthorizederror_if_user_not_found_in_database(clean_database):
#     """ identify gets token and if user couldn't be found raise NotAuthorizedError """
#     invalid_token = jwt.encode(
#         {
#             "user_id": 123,
#             "iat": datetime.utcnow(),
#             "exp": datetime.utcnow() + timedelta(days=config["JWT_ACCESS_TOKEN_EXPIRES"])
#         },
#         config["JWT_SECRET_KEY"],
#         algorithm=ALGORITHM
#     )
#     with pytest.raises(NotAuthorizedError) as errorval:
#         identify(invalid_token)
#     assert isinstance(errorval.value, NotAuthorizedError)
