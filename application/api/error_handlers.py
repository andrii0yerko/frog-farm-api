from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
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


@bp.app_errorhandler(HTTPException)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return error_response(e.code, e.description)

    # now you're handling non-HTTP exceptions only
    return error_response(500)


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return error_response(500)


@bp.app_errorhandler(IntegrityError)
def integrity_error(e):
    db.session.rollback()
    return error_response(400, 'Integrity error, some DB constraints violated')


@auth.error_handler
def basic_auth_error():
    return error_response(401)