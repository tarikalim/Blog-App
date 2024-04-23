from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields
from Service.UserService import *

user_ns = Namespace('user', description='User operations')

user_model = user_ns.model('User', {
    'id': fields.Integer(required=True, description='User ID'),
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
    'join_date': fields.DateTime(description='Join Date'),
})


@user_ns.route('/int:<user_id>')
class UserResource(Resource):
    @jwt_required()
    @user_ns.marshal_with(user_model)
    def get(self, user_id):
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return {'message': 'You can only view your own profile.'}, 403

        user = UserService.get_user_by_id(user_id)
        return user

    @jwt_required()
    @user_ns.expect(user_model, validate=True)
    @user_ns.marshal_with(user_model)
    def put(self, user_id):
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return {'message': 'You can only update your own profile.'}, 403

        data = user_ns.payload
        user = UserService.update_user(user_id, username=data['username'], email=data['email'])
        return user

    @jwt_required()
    def delete(self, user_id):
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return {'message': 'You can only delete your own profile.'}, 403

        UserService.delete_user(user_id)
        return {'message': 'User deleted successfully.'}, 200
