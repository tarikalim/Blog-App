from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields
from Service.CommentService import *
from extensions import api

comment_ns = Namespace('comment', description='Comment operations')

comment_model = comment_ns.model('Comment', {
    'id': fields.Integer(required=True, description='Comment ID'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'post_id': fields.Integer(required=True, description='Post ID'),
    'content': fields.String(required=True, description='Content'),
    'comment_date': fields.DateTime(description='Comment Date'),
})

create_comment_model = comment_ns.model('CreateComment', {
    'content': fields.String(required=True, description='Content'),
})
delete_comment_model = comment_ns.model('DeleteComment', {
    'comment_id': fields.Integer(required=True, description='Comment ID'),
})
update_comment_model = comment_ns.model('UpdateComment', {
    'content': fields.String(required=True, description='Content'),
})

comment_user_model = comment_ns.model('CommentUser', {
    'id': fields.Integer(required=True, description='User ID'),
    'username': fields.String(required=True, description='Username'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'post_id': fields.Integer(required=True, description='Post ID'),
    'content': fields.String(required=True, description='Content'),
    'comment_date': fields.DateTime(description='Comment Date'),
})


@api.errorhandler(CommentNotFoundException)
def handle_comment_not_found_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(DatabaseOperationException)
def handle_database_operation_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(AuthorizationException)
def handle_authorization_exception(error):
    return {'message': error.message}, error.status_code


@comment_ns.route('/<int:post_id>')
class CommentsResource(Resource):
    @comment_ns.marshal_list_with(comment_user_model)
    @comment_ns.doc(description='Get all comments for a post')
    def get(self, post_id):
        """Get all comments for a post."""
        return CommentService.get_post_comments(post_id)

    @jwt_required()
    @comment_ns.expect(create_comment_model, validate=True)
    @comment_ns.marshal_with(comment_model)
    @comment_ns.doc(description='Create a new comment')
    def post(self, post_id):
        """Create a new comment for a post. User must be logged in."""
        current_user_id = get_jwt_identity()
        data = comment_ns.payload
        return CommentService.create_comment(user_id=current_user_id, post_id=post_id,
                                             content=data['content'])


@comment_ns.route('/<int:comment_id>')
class CommentResource(Resource):
    @jwt_required()
    @comment_ns.doc(description='Delete a comment')
    def delete(self, comment_id):
        """Delete a comment. User must be logged in and only the owner can delete the comment."""
        current_user_id = get_jwt_identity()
        comment = CommentService.get_comment_by_id(comment_id)
        if comment.user_id != current_user_id:
            raise AuthorizationException('You can only delete your own comments')
        CommentService.delete_comment(comment_id)
        return '', 204

    @jwt_required()
    @comment_ns.expect(update_comment_model, validate=True)
    @comment_ns.marshal_with(comment_model)
    @comment_ns.doc(description='Update a comment')
    def put(self, comment_id):
        """Update a comment. User must be logged in and only the owner can update the comment."""
        current_user_id = get_jwt_identity()
        comment = CommentService.get_comment_by_id(comment_id)
        if comment.user_id != current_user_id:
            raise AuthorizationException('You can only update your own comments')
        data = comment_ns.payload
        return CommentService.update_comment(comment_id=comment_id, content=data['content']), 200
