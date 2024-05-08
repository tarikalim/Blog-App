from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields
from Service.LikeService import *
from extensions import api

# Namespace
like_ns = Namespace('like', description='Handle likes on posts')

# Models
like_model = like_ns.model('Like', {
    'user_id': fields.Integer(description='User ID of the liker'),
    'post_id': fields.Integer(description='Post ID'),
})

like_count_model = like_ns.model('LikeCount', {
    'like_count': fields.Integer(description='Total number of likes'),
})


@api.errorhandler(LikeAlreadyExistsException)
def handle_like_already_exists_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(LikeNotFoundException)
def handle_like_not_found_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(PostNotFoundException)
def handle_post_not_found_exception(error):
    return {'message': error.message}, error.status_code


# Like operations
@like_ns.route('/<int:post_id>')
class LikeResource(Resource):
    # Like a post
    @jwt_required()
    @like_ns.marshal_with(like_model)
    def post(self, post_id):
        user_id = get_jwt_identity()
        return LikeService.create_like(user_id, post_id)

    # Get the number of likes on a post
    @like_ns.marshal_with(like_count_model)
    def get(self, post_id):
        return LikeService.get_post_likes(post_id)

    # Unlike a post
    @jwt_required()
    def delete(self, post_id):
        user_id = get_jwt_identity()
        LikeService.delete_like(user_id, post_id)
        return "", 204
