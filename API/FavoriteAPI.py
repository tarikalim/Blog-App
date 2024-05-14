from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields
from Service.FavoriteService import *
from extensions import api

favorite_ns = Namespace('favorite', description='Favorite operations')

favorite_model = favorite_ns.model('Favorite', {
    'id': fields.Integer(required=True, description='Favorite ID'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'post_id': fields.Integer(required=True, description='Post ID'),
    'title': fields.String(description='Title'),
    'content': fields.String(description='Content'),
})

user_favorite_status_model = favorite_ns.model('UserFavoriteStatus', {
    'user_id': fields.Integer(description='User ID of the favoriter'),
    'post_id': fields.Integer(description='Post ID'),
    'status': fields.Boolean(description='True if user has favorited the post, False otherwise')
})


@api.errorhandler(FavoriteNotFoundException)
def handle_favorite_not_found_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(PostNotFoundException)
def handle_post_not_found_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(FavoriteAlreadyExistsException)
def handle_favorite_already_exists_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(AuthorizationException)
def handle_authorization_exception(error):
    return {'message': error.message}, error.status_code


@favorite_ns.route('/user')
class UserFavoritesResource(Resource):

    @jwt_required()
    @favorite_ns.marshal_list_with(favorite_model)
    @favorite_ns.doc(description='Get all favorites of current user.')
    def get(self):
        """Get all favorites of the current user."""
        user_id = get_jwt_identity()
        return FavoriteService.get_favorites_by_user_id(user_id)


@favorite_ns.route('/<int:post_id>')
class FavoriteResource(Resource):

    @jwt_required()
    @favorite_ns.marshal_with(favorite_model)
    def post(self, post_id):
        """Create a favorite. token required."""
        user_id = get_jwt_identity()
        return FavoriteService.create_favorite(user_id, post_id)


@favorite_ns.route('/<int:favorite_id>')
class FavoriteResource(Resource):

    @jwt_required()
    def delete(self, favorite_id):
        """Delete a favorite. token required."""
        current_user_id = get_jwt_identity()
        favorite = FavoriteService.get_favorite_by_id(favorite_id)
        if favorite.user_id != current_user_id:
            raise AuthorizationException('You are not authorized to delete this favorite.')
        return FavoriteService.delete_favorite(favorite_id)


@favorite_ns.route('/status/<int:post_id>')
class FavoriteStatusResource(Resource):

    @jwt_required()
    @favorite_ns.marshal_with(user_favorite_status_model)
    def get(self, post_id):
        """Get the status of a user's favorite on a post. token required."""
        user_id = get_jwt_identity()
        return FavoriteService.get_user_favorite_status(user_id, post_id)
