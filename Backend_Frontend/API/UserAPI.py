from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields, reqparse, marshal_with
from Backend_Frontend.Service.UserService import *

user_ns = Namespace('user', description='User operations')

user_model = user_ns.model('User', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
    'join_date': fields.DateTime(description='Join Date'),
    'id': fields.Integer(description='User ID')
})
update_user_model = user_ns.model('UpdateUser', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
})


# user specific operations
@user_ns.route('/')
class UserResource(Resource):
    method_decorators = [jwt_required()]

    @marshal_with(user_model)
    def get(self):
        """Get current user information from token"""
        current_user_id = get_jwt_identity()
        return UserService.get_user_by_id(current_user_id)

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
        return UserService.update_user(current_user_id, **data)


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
        return UserService.get_users_by_username(username)
