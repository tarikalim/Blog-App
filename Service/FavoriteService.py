from Model.model import db, Favorite, Post
from Exception.exception import *


class FavoriteDTO:
    def __init__(self, favorite):
        self.id = favorite.id
        self.user_id = favorite.user_id
        self.post_id = favorite.post_id


class FavoritePostDTO:
    def __init__(self, favorite, post_title, post_content):
        self.id = favorite.id
        self.user_id = favorite.user_id
        self.post_id = favorite.post_id
        self.title = post_title
        self.content = post_content


class FavoriteService:

    @staticmethod
    def get_favorites_by_user_id(user_id):
        results = db.session.query(Favorite, Post.title, Post.content).join(Post).filter(
            Favorite.user_id == user_id).all()
        favorites_data = []
        for favorite, post_title, post_content in results:
            favorite_data = FavoritePostDTO(favorite, post_title, post_content)
            favorites_data.append(favorite_data)
        return favorites_data

    @staticmethod
    def get_favorite_by_id(favorite_id):
        result = db.session.query(Favorite, Post.title, Post.content).join(Post).filter(
            Favorite.id == favorite_id).first()
        if not result:
            raise FavoriteNotFoundException()

        favorite, post_title, post_content = result
        return FavoritePostDTO(favorite, post_title, post_content)

    @staticmethod
    def create_favorite(user_id, post_id):
        post = Post.query.get(post_id)
        if not post:
            raise PostNotFoundException()
        existing_favorite = Favorite.query.filter_by(user_id=user_id, post_id=post_id).first()
        if existing_favorite:
            raise FavoriteAlreadyExistsException()

        new_favorite = Favorite(
            user_id=user_id,
            post_id=post_id
        )

        db.session.add(new_favorite)
        db.session.commit()

        return FavoritePostDTO(new_favorite, post.title, post.content)

    @staticmethod
    def delete_favorite(favorite_id):
        favorite = Favorite.query.get(favorite_id)
        if not favorite:
            raise FavoriteNotFoundException()
        db.session.delete(favorite)
        db.session.commit()
        return None
