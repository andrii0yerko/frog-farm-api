from core import db, jwt
from . import bp
from .error import error_response


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return error_response(500)


@jwt.invalid_token_loader
def invalid_token(reason):
    return error_response(401, reason)


@jwt.expired_token_loader
def invalid_token(header, payload):
    return error_response(401, "Token has expired")