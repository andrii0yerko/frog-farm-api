from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from sqlalchemy.exc import IntegrityError

from core import db
from . import bp, auth


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return error_response(500)


@auth.error_handler
def basic_auth_error():
    return error_response(401)
