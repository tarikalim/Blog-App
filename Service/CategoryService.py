from Model.model import Category


class CategoryService:

    @staticmethod
    def get_all_categories():
        return Category.query.all()

    @staticmethod
    def get_category_name_by_id(category_id):
        category = Category.query.get(category_id)
        return category
