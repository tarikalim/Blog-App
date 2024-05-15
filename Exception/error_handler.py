from flask_restx import Api
from Exception.exception import ApplicationException


def error_handler(api: Api):
    @api.errorhandler(ApplicationException)
    def handle_application_exception(error):
        return {'message': error.message}, error.status_code
