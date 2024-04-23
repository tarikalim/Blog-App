from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields, reqparse
from Service.PostService import PostService

post_ns = Namespace('post', description='Post operations')

post_model = post_ns.model('Post', {
    'user_id': fields.Integer(required=True, description='User ID'),
    'title': fields.String(required=True, description='Title'),
    'content': fields.String(required=True, description='Content'),
    'publish_date': fields.DateTime(description='Publish Date'),
    'category_id': fields.Integer(required=True, description='Category ID'),
})
create_post_model = post_ns.model('CreatePost', {
    'title': fields.String(required=True, description='Title'),
    'content': fields.String(required=True, description='Content'),
    'category_id': fields.Integer(required=True, description='Category ID'),
})
update_post_model = post_ns.model('UpdatePost', {
    'title': fields.String(required=True, description='Title'),
    'content': fields.String(required=True, description='Content'),
    'category_id': fields.Integer(required=True, description='Category ID'),
})
find_post_model = post_ns.model('FindPost', {
    'title': fields.String(description='Title to filter posts'),
    'content': fields.String(description='Content to filter posts')
})


# posts related operations
@post_ns.route('')
class PostsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help='Title to filter posts')

    # get all posts or filter by title
    @post_ns.expect(parser)
    @post_ns.marshal_list_with(find_post_model)
    def get(self):
        title = self.parser.parse_args().get('title')
        if title:
            posts = PostService.get_posts_by_title(title)
        else:
            posts = PostService.get_all_posts()
        return posts

    # create a post
    @jwt_required()
    @post_ns.expect(create_post_model, validate=True)
    @post_ns.marshal_with(post_model)
    @post_ns.doc(summary='Create a new post')
    def post(self):
        current_user_id = get_jwt_identity()
        data = post_ns.payload
        post = PostService.create_post(user_id=current_user_id, title=data['title'], content=data['content'],
                                       category_id=data['category_id'])
        return post, 201


# post specific operations
@post_ns.route('/<int:post_id>')
class PostResource(Resource):
    # get a post by ID
    @post_ns.marshal_with(post_model)
    @post_ns.doc(description='Get a post by its ID.')
    def get(self, post_id):
        post = PostService.get_post_by_id(post_id)
        if post is None:
            return {'message': 'Post not found.'}, 404
        return post

    # update a post by ID
    @jwt_required()
    @post_ns.expect(update_post_model, validate=True)
    @post_ns.marshal_with(post_model)
    @post_ns.doc(description='Update a post by ID')
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

    # delete a post by ID
    @jwt_required()
    @post_ns.doc(description='Delete a post by ID')
    def delete(self, post_id):
        current_user_id = get_jwt_identity()
        post = PostService.get_post_by_id(post_id)
        if post is None:
            return {'message': 'Post not found.'}, 404
        if post.user_id != current_user_id:
            return {'message': 'You can only delete your own posts.'}, 403

        PostService.delete_post(post_id)
        return {'message': 'Post deleted successfully.'}, 200
