from core import db
from . import bp
from .auth import auth
from .error import error_response

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return error_response(500)


@auth.error_handler
def basic_auth_error():
    return error_response(401)
