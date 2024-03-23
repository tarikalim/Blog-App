from flask_restx import Resource, Namespace, fields
from Service.AuthService import *

auth_ns = Namespace('auth', description='Authentication  operations')

user_registration_model = auth_ns.model('UserRegistration', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})

user_login_model = auth_ns.model('UserLogin', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})


@auth_ns.route('/register')
class UserRegistration(Resource):
    @auth_ns.expect(user_registration_model, validate=True)
    def post(self):
        data = auth_ns.payload
        user = AuthService.register_user(username=data['username'],
                                         email=data['email'],
                                         password=data['password']
                                         )
        if user:
            return {'message': 'User created successfully.'}, 201
        else:
            auth_ns.abort(409, 'User already exists.')


@auth_ns.route('/login')
class UserLogin(Resource):
    @auth_ns.expect(user_login_model, validate=True)
    def post(self):
        data = auth_ns.payload
        token = AuthService.login_user(username=data['username'], password=data['password'])
        if token:
            return {'token': token}, 200
        else:
            auth_ns.abort(401, 'Invalid credentials')
