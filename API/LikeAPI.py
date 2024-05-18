from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields
from Service.LikeService import *

# Namespace
like_ns = Namespace('like', description='Handle likes on posts')

# Models
like_model = like_ns.model('Like', {
    'user_id': fields.Integer(description='User ID of the liker'),
    'post_id': fields.Integer(description='Post ID'),
})
user_like_status_model = like_ns.model('UserLikeStatus', {
    'user_id': fields.Integer(description='User ID of the liker'),
    'post_id': fields.Integer(description='Post ID'),
    'status': fields.Boolean(description='True if user has liked the post, False otherwise')
})

like_count_model = like_ns.model('LikeCount', {
    'like_count': fields.Integer(description='Total number of likes'),
})

user_like_post_model = like_ns.model('UserLikePost', {
    'post_id': fields.Integer(description='Post ID'),
    'title': fields.String(description='Title of the post'),
})


# Like operations
@like_ns.route('/<int:post_id>')
class LikeResource(Resource):
    # Like a post
    @jwt_required()
    @like_ns.marshal_with(like_model)
    def post(self, post_id):
        """Like a post, User must be logged in."""
        user_id = get_jwt_identity()
        return LikeService.create_like(user_id, post_id)

    # Get the number of likes on a post
    @like_ns.marshal_with(like_count_model)
    def get(self, post_id):
        """Get the number of likes on a post."""
        return LikeService.get_post_likes(post_id)

    # Unlike a post
    @jwt_required()
    def delete(self, post_id):
        """Unlike a post, User must be logged in."""
        user_id = get_jwt_identity()
        LikeService.delete_like(user_id, post_id)
        return "", 204

    @like_ns.route('/status/<int:post_id>')
    class LikeStatusResource(Resource):
        # Get the status of a user's like on a post
        @jwt_required()
        @like_ns.marshal_with(user_like_status_model)
        def get(self, post_id):
            """Get the status of a user's like on a post, User must be logged in."""
            user_id = get_jwt_identity()
            return LikeService.get_user_like_status(user_id, post_id)


@like_ns.route('/user')
class UserLikePostResource(Resource):
    # Get all posts liked by the user
    @jwt_required()
    @like_ns.marshal_with(user_like_post_model)
    def get(self):
        """Get all posts liked by the user, User must be logged in."""
        user_id = get_jwt_identity()
        return LikeService.get_user_liked_posts(user_id)
