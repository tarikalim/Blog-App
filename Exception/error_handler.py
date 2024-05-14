from flask_jwt_extended.exceptions import JWTExtendedException
from flask_restx import Api
from Exception.exception import ApplicationException


def error_handler(api: Api):
    @api.errorhandler(ApplicationException)
    def handle_application_exception(error):
        return {'message': error.message}, error.status_code

    @api.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, (JWTExtendedException, ApplicationException)):
            raise error
        else:
            return {'message': 'An unexpected error occurred'}, 500
