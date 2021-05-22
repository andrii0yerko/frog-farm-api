from core import jwt
from .error import error_response

errors = {
    "ExpiredSignatureError": error_response(401, "[]Token has expired"),
    "InvalidTokenError": error_response(401, "[]Invalid token")
}


@jwt.invalid_token_loader
def invalid_token(reason):
    return error_response(401, reason)


@jwt.expired_token_loader
def expired_token(header, payload):
    return error_response(401, "Token has expired")