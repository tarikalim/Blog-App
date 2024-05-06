from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields, reqparse, marshal_with
from Service.UserService import *
from extensions import api

user_ns = Namespace('user', description='User operations')

user_model = user_ns.model('User', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
    'join_date': fields.DateTime(description='Join Date'),
})
update_user_model = user_ns.model('UpdateUser', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
})


@api.errorhandler(UserNotFoundException)
def handle_user_not_found_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(UserAlreadyExistsException)
def handle_user_already_exists_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(DatabaseOperationException)
def handle_database_operation_exception(error):
    return {'message': error.message}, error.status_code


# user specific operations
@user_ns.route('/')
class UserResource(Resource):
    method_decorators = [jwt_required()]

    @marshal_with(user_model)
    def get(self):
        """Get current user information from token"""
        current_user_id = get_jwt_identity()
        return UserService.get_user_by_id(current_user_id)

    @marshal_with(user_model)
    def delete(self):
        """Delete current user account and all related data"""
        current_user_id = get_jwt_identity()
        UserService.delete_user(current_user_id)
        return '', 204

    @user_ns.expect(update_user_model, validate=True)
    @marshal_with(user_model)
    def put(self):
        """Update current user information"""
        current_user_id = get_jwt_identity()
        data = user_ns.payload
        user = UserService.update_user(current_user_id, **data)
        return user


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=False, help='Username to filter users')


@user_ns.route('/search')
class UserSearch(Resource):
    # search users by username
    @user_ns.expect(parser)
    @user_ns.marshal_list_with(user_model)
    def get(self):
        """Search users by username"""
        args = parser.parse_args()
        username = args.get('username')
        if username:
            users = UserService.get_users_by_username(username)
        else:
            users = UserService.get_all_users()
        return users
