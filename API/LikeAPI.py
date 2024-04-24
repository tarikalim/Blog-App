from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields, reqparse
from Service.LikeService import LikeService

like_ns = Namespace('like', description='Like operations')

like_model = like_ns.model('Like', {
    'user_id': fields.Integer(required=True, description='User ID'),
    'post_id': fields.Integer(required=True, description='Post ID'),
})
create_like_model = like_ns.model('CreateLike', {
    'post_id': fields.Integer(required=True, description='Post ID'),
})

find_like_model = like_ns.model('FindLike', {
    'post_id': fields.Integer(description='Post ID to filter likes'),
    'like_count': fields.Integer(description='Total number of likes for the post')
})


@like_ns.route('')
class LikeResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('post_id', type=int, help='Post ID to filter likes')

    # get total likes of a post
    @like_ns.expect(parser)
    @like_ns.marshal_list_with(find_like_model)
    def get(self):
        post_id = self.parser.parse_args().get('post_id')
        if post_id:
            like_count = LikeService.get_post_likes(post_id)
            return {'post_id': post_id, 'like_count': like_count}
        else:
            return {'message': 'Post ID is required'}, 400

    # create a like
    @jwt_required()
    @like_ns.expect(create_like_model, validate=True)
    @like_ns.marshal_with(like_model)
    @like_ns.doc(summary='Create a new like')
    def post(self):
        current_user_id = get_jwt_identity()
        data = like_ns.payload
        like = LikeService.create_like(user_id=current_user_id, post_id=data['post_id'])
        return like, 201


@like_ns.route('/<int:like_id>')
class LikeResource(Resource):
    # delete a like
    @jwt_required()
    @like_ns.doc(description='Delete a like')
    def delete(self, like_id):
        current_user_id = get_jwt_identity()
        success, message = LikeService.delete_like(like_id=like_id, user_id=current_user_id)
        if success:
            return message, 200
        return message, 403
