from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields, reqparse
from Service.PostService import *

post_ns = Namespace('post', description='Post operations')

post_model = post_ns.model('Post', {
    'id': fields.Integer(required=True, description='Post ID'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'title': fields.String(required=True, description='Title'),
    'content': fields.String(required=True, description='Content'),
    'publish_date': fields.DateTime(description='Publish Date of the post', dt_format='rfc822'),
    'category_id': fields.Integer(required=True, description='Category ID'),
    'category_name': fields.String(description='Category Name'),
})
create_post_model = post_ns.model('CreatePost', {
    'title': fields.String(required=True, description='Title'),
    'content': fields.String(required=True, description='Content'),
    'category_id': fields.Integer(required=True, description='Category ID'),
})
update_post_model = post_ns.model('UpdatePost', {
    'title': fields.String(required=True, description='Title'),
    'content': fields.String(required=True, description='Content'),
})


# posts related operations

@post_ns.route('/user')
class UserPostsResource(Resource):

    @jwt_required()
    @post_ns.marshal_list_with(post_model)
    @post_ns.doc(description='Get all posts of current user.')
    def get(self):
        """Get all posts of the current user."""
        user_id = get_jwt_identity()
        return PostService.get_user_posts(user_id)


@post_ns.route('')
class PostsResource(Resource):

    # create a post
    @jwt_required()
    @post_ns.expect(create_post_model, validate=True)
    @post_ns.marshal_with(post_model)
    def post(self):
        """Create a new post. User must be logged in."""
        current_user_id = get_jwt_identity()
        data = post_ns.payload
        return PostService.create_post(user_id=current_user_id, title=data['title'], content=data['content'],
                                       category_id=data['category_id'])


@post_ns.route('/<int:post_id>')
class PostResource(Resource):
    """Get a post by its ID."""

    @post_ns.marshal_with(post_model)
    @post_ns.doc(description='Get a post by its ID.')
    def get(self, post_id):
        """Get a post by its ID."""
        return PostService.get_post_by_id(post_id)

    @jwt_required()
    @post_ns.expect(update_post_model, validate=True)
    @post_ns.marshal_with(post_model)
    @post_ns.doc(description='Update a post by ID')
    def put(self, post_id):
        """Update a post by ID. User must be logged in and only the owner can update the post."""
        current_user_id = get_jwt_identity()
        post = PostService.get_post_by_id(post_id)
        if post.user_id != current_user_id:
            raise AuthorizationException('You can only update your own posts')

        data = post_ns.payload
        return PostService.update_post(post_id, title=data['title'], content=data['content'])

    @jwt_required()
    @post_ns.doc(description='Delete a post by ID')
    def delete(self, post_id):
        """Delete a post by ID. User must be logged in and only the owner can delete the post."""
        current_user_id = get_jwt_identity()
        post = PostService.get_post_by_id(post_id)
        if post.user_id != current_user_id:
            raise AuthorizationException('You can only delete your own posts')
        PostService.delete_post(post_id)
        return "", 204


@post_ns.route('/category/<int:category_id>')
class CategoryPostsResource(Resource):
    @post_ns.marshal_list_with(post_model)
    def get(self, category_id):
        """Get all posts of a category by its ID."""
        return PostService.get_posts_by_category(category_id)


@post_ns.route('/search')
class PostsSearchResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help='Title to filter posts', location='args')

    @post_ns.expect(parser)
    @post_ns.marshal_list_with(post_model)
    def get(self):
        """Get all posts or filter by title."""
        args = self.parser.parse_args()
        title = args['title']
        if title:
            posts = PostService.get_posts_by_title(title)
        else:
            posts = PostService.get_all_posts()
        return posts
