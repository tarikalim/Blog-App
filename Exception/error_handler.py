from flask_jwt_extended.exceptions import JWTExtendedException
from sqlalchemy.exc import SQLAlchemyError
from Exception.exception import ApplicationException
from flask_restx import Api

from extensions import db


def error_handler(api: Api):
    @api.errorhandler(ApplicationException)
    def handle_application_exception(error):

        return {'message': error.message}, error.status_code

    @api.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        db.session.rollback()
        return {'message': 'A database error occurred', 'details': str(error)}, 500

    @api.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, (ApplicationException, JWTExtendedException, SQLAlchemyError)):
            raise error
        else:
            return {'message': 'An unexpected error occurred', 'details': str(error)}, 500
