from Model.model import db, Post, Category


class PostService:
    @staticmethod
    def get_all_posts():
        results = db.session.query(Post, Category.name).join(Category).all()
        posts_data = []
        for post, category_name in results:
            post_data = {
                'id': post.id,
                'user_id': post.user_id,
                'title': post.title,
                'content': post.content,
                'publish_date': post.publish_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),  # RFC822 format
                'category_id': post.category_id,
                'category_name': category_name
            }
            posts_data.append(post_data)
        return posts_data if posts_data else None

    @staticmethod
    def get_user_posts(user_id):
        results = db.session.query(Post, Category.name).join(Category).filter(Post.user_id == user_id).all()
        posts_data = []
        for post, category_name in results:
            post_data = {
                'id': post.id,
                'user_id': post.user_id,
                'title': post.title,
                'content': post.content,
                'publish_date': post.publish_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),  # RFC822 format
                'category_id': post.category_id,
                'category_name': category_name
            }
            posts_data.append(post_data)
        return posts_data if posts_data else None

    @staticmethod
    def get_post_by_id(post_id):
        result = db.session.query(Post, Category.name).join(Category).filter(Post.id == post_id).first()
        if result:
            post, category_name = result
            post_data = {
                'id': post.id,
                'user_id': post.user_id,
                'title': post.title,
                'content': post.content,
                'publish_date': post.publish_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),  # RFC822 format
                'category_id': post.category_id,
                'category_name': category_name
            }
            return post_data
        return None

    @staticmethod
    def get_posts_by_title(title):
        results = db.session.query(Post, Category.name).join(Category, Post.category_id == Category.id).filter(
            Post.title.like(f'%{title}%')).all()
        posts_data = []
        for post, category_name in results:
            post_data = {
                'id': post.id,
                'user_id': post.user_id,
                'title': post.title,
                'content': post.content,
                'publish_date': post.publish_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
                'category_id': post.category_id,
                'category_name': category_name
            }
            posts_data.append(post_data)
        return posts_data if posts_data else None

    @staticmethod
    def get_posts_by_category(category_id):
        results = db.session.query(Post, Category.name).join(Category, Post.category_id == Category.id).filter(
            Post.category_id == category_id).all()
        posts_data = []
        for post, category_name in results:
            post_data = {
                'id': post.id,
                'user_id': post.user_id,
                'title': post.title,
                'content': post.content,
                'publish_date': post.publish_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
                'category_id': post.category_id,
                'category_name': category_name
            }
            posts_data.append(post_data)
        return posts_data if posts_data else None

    @staticmethod
    def create_post(user_id, title, content, category_id):
        new_post = Post(
            user_id=user_id,
            title=title,
            content=content,
            category_id=category_id
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post

    @staticmethod
    def update_post(post_id, title=None, content=None):
        post = Post.query.get(post_id)
        if title:
            post.title = title
        if content:
            post.content = content
        db.session.commit()
        return post

    @staticmethod
    def delete_post(post_id):
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()
        return post
