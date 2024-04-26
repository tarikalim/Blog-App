from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields, reqparse
from Service.UserService import *

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


# user specific operations
@user_ns.route('')
class UserResource(Resource):
    # get your info
    @jwt_required()
    @user_ns.marshal_with(user_model)
    def get(self):
        current_user_id = get_jwt_identity()
        user = UserService.get_user_by_id(current_user_id)
        return user

    # update your info
    @jwt_required()
    @user_ns.expect(update_user_model, validate=True)
    @user_ns.marshal_with(user_model)
    def put(self):
        current_user_id = get_jwt_identity()
        data = user_ns.payload
        user = UserService.update_user(current_user_id, username=data['username'], email=data['email'])
        return user


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=False, help='Username to filter users')


@user_ns.route('/search')
class UserSearch(Resource):
    # search users by username
    @user_ns.expect(parser)
    @user_ns.marshal_list_with(user_model)
    def get(self):
        args = parser.parse_args()
        username = args.get('username')
        if username:
            users = UserService.get_users_by_username(username)
        else:
            users = UserService.get_all_users()
        return users
