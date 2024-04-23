from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields
from Service.UserService import UserService
from Service.PostService import PostService

post_ns = Namespace('post', description='Post operations')

post_model = post_ns.model('Post', {
    'id': fields.Integer(required=True, description='Post ID'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'title': fields.String(required=True, description='Title'),
    'content': fields.String(required=True, description='Content'),
    'publish_date': fields.DateTime(description='Publish Date'),
    'category_id': fields.Integer(required=True, description='Category ID'),
})


@post_ns.route('/<int:post_id>')
class PostResource(Resource):
    @post_ns.marshal_with(post_model)
    def get(self, post_id):
        post = PostService.get_post_by_id(post_id)
        if post is None:
            return {'message': 'Post not found.'}, 404
        return post

    @jwt_required()
    @post_ns.expect(post_model, validate=True)
    @post_ns.marshal_with(post_model)
    def put(self, post_id):
        current_user_id = get_jwt_identity()
        post = PostService.get_post_by_id(post_id)
        if post is None:
            return {'message': 'Post not found.'}, 404
        if post.user_id != current_user_id:
            return {'message': 'You can only update your own posts.'}, 403

        data = post_ns.payload
        updated_post = PostService.update_post(post_id, title=data['title'], content=data['content'])
        return updated_post

    @jwt_required()
    def delete(self, post_id):
        current_user_id = get_jwt_identity()
        post = PostService.get_post_by_id(post_id)
        if post is None:
            return {'message': 'Post not found.'}, 404
        if post.user_id != current_user_id:
            return {'message': 'You can only delete your own posts.'}, 403

        PostService.delete_post(post_id)
        return {'message': 'Post deleted successfully.'}, 200


@post_ns.route('/user/<int:user_id>')
class UserPosts(Resource):
    @post_ns.marshal_list_with(post_model)
    def get(self, user_id):
        posts = PostService.get_user_posts(user_id)
        if not posts:
            return {'message': 'No posts found for this user.'}, 404
        return posts
