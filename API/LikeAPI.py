from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields, abort

from Service.LikeService import LikeService

# Namespace
like_ns = Namespace('likes', description='Handle likes on posts')

# Models
like_model = like_ns.model('Like', {
    'user_id': fields.Integer(description='User ID of the liker'),
    'post_id': fields.Integer(description='Post ID'),
})

like_count_model = like_ns.model('LikeCount', {
    'post_id': fields.Integer(description='Post ID'),
    'like_count': fields.Integer(description='Total number of likes'),
})


# Like operations
@like_ns.route('/<int:post_id>')
class LikeResource(Resource):
    # Like a post
    @jwt_required()
    @like_ns.marshal_with(like_model)
    def post(self, post_id):
        user_id = get_jwt_identity()
        new_like = LikeService.create_like(user_id, post_id)
        if new_like is None:
            return abort(409, 'Post already liked.')
        return new_like, 201

    @jwt_required()
    @like_ns.marshal_with(like_count_model)
    def get(self, post_id):
        like_count = LikeService.get_post_likes(post_id)
        return {
            'post_id': post_id,
            'like_count': like_count
        }

    # Unlike a post
    @jwt_required()
    def delete(self, post_id):
        user_id = get_jwt_identity()
        success, message = LikeService.delete_like(user_id, post_id)
        if not success:
            abort(404, message)
        return {'message': message}, 200
