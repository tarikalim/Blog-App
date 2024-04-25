from flask_restx import Resource, Namespace, fields
from Service.CategoryService import CategoryService

category_ns = Namespace('category', description='Category operations')

category_model = category_ns.model('Category', {
    'id': fields.Integer(required=True, description='Category ID'),
    'name': fields.String(required=True, description='Category Name'),
    'description': fields.String(required=True, description='Category Description')
})
category_name_model = category_ns.model('Category Name', {
    'name': fields.String(required=True, description='Category Name')
})


@category_ns.route('')
class CategoryResource(Resource):
    @category_ns.marshal_with(category_model)
    @category_ns.doc(description='Get all categories')
    def get(self):
        return CategoryService.get_all_categories()


@category_ns.route('/<int:category_id>')
class CategoryResource(Resource):
    @category_ns.marshal_with(category_name_model)
    @category_ns.doc(description='Get category name by ID')
    def get(self, category_id):
        return CategoryService.get_category_name_by_id(category_id)
