from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields, reqparse
from Service.CommentService import CommentService

comment_ns = Namespace('comment', description='Comment operations')

comment_model = comment_ns.model('Comment', {
    'user_id': fields.Integer(required=True, description='User ID'),
    'post_id': fields.Integer(required=True, description='Post ID'),
    'content': fields.String(required=True, description='Content'),
    'comment_date': fields.DateTime(description='Comment Date'),
})

create_comment_model = comment_ns.model('CreateComment', {
    'post_id': fields.Integer(required=True, description='Post ID'),
    'content': fields.String(required=True, description='Content'),
})
delete_comment_model = comment_ns.model('DeleteComment', {
    'comment_id': fields.Integer(required=True, description='Comment ID'),
})
update_comment_model = comment_ns.model('UpdateComment', {
    'content': fields.String(required=True, description='Content'),
})


@comment_ns.route('')
class CommentsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('post_id', type=int, help='Post ID to filter comments')

    @comment_ns.expect(parser)
    @comment_ns.marshal_list_with(comment_model)
    @comment_ns.doc(description='Get all comments or filter by post_id')
    def get(self):
        post_id = self.parser.parse_args().get('post_id')
        if post_id:
            comments = CommentService.get_post_comments(post_id)
        else:
            comments = CommentService.get_all_comments()
        return comments

    @jwt_required()
    @comment_ns.expect(create_comment_model, validate=True)
    @comment_ns.marshal_with(comment_model)
    @comment_ns.doc(description='Create a new comment')
    def post(self):
        current_user_id = get_jwt_identity()
        data = comment_ns.payload
        comment = CommentService.create_comment(user_id=current_user_id, post_id=data['post_id'],
                                                content=data['content'])
        return comment, 201


@comment_ns.route('/<int:comment_id>')
class CommentResource(Resource):
    @jwt_required()
    @comment_ns.doc(description='Delete a comment')
    def delete(self, comment_id):
        current_user_id = get_jwt_identity()
        success, message = CommentService.delete_comment(comment_id=comment_id, user_id=current_user_id)
        if success:
            return {'message': message}, 200
        return {'message': message}, 403

    @jwt_required()
    @comment_ns.expect(update_comment_model, validate=True)
    @comment_ns.marshal_with(comment_model)
    @comment_ns.doc(description='Update a comment')
    def put(self, comment_id):
        current_user_id = get_jwt_identity()
        data = comment_ns.payload
        comment = CommentService.update_comment(comment_id=comment_id, user_id=current_user_id,
                                                content=data['content'])
        if comment:
            return comment
        return {'message': 'You are not the owner of this comment'}, 403
