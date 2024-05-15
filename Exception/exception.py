class ApplicationException(Exception):
    """Base exception class for all application-specific errors."""

    def __init__(self, message="An error occurred", status_code=500):
        self.message = message
        self.status_code = status_code


class UserNotFoundException(ApplicationException):
    """Exception raised when a user is not found."""

    def __init__(self, message="User not found"):
        super().__init__(message, status_code=404)


class UserAlreadyExistsException(ApplicationException):
    """Exception raised when a user already exists."""

    def __init__(self, message="User already exists"):
        super().__init__(message, status_code=400)


class PostNotFoundException(ApplicationException):
    """Exception raised when a post is not found."""

    def __init__(self, message="Post not found"):
        super().__init__(message, status_code=404)


class PostCreationFailedException(ApplicationException):
    """Exception raised when post creation fails."""

    def __init__(self, message="Post creation failed"):
        super().__init__(message, status_code=500)


class PostUpdateFailedException(ApplicationException):
    """Exception raised when post update fails."""

    def __init__(self, message="Post update failed"):
        super().__init__(message, status_code=500)


class PostDeletionFailedException(ApplicationException):
    """Exception raised when post deletion fails."""

    def __init__(self, message="Post deletion failed"):
        super().__init__(message, status_code=500)


class CategoryNotFoundException(ApplicationException):
    """Exception raised when a category is not found."""

    def __init__(self, message="Category not found"):
        super().__init__(message, status_code=404)


class DatabaseOperationException(ApplicationException):
    """Exception raised for database operation failures."""

    def __init__(self, message="Database operation failed"):
        super().__init__(message, status_code=500)


class CommentNotFoundException(ApplicationException):
    """Exception raised when a comment is not found."""

    def __init__(self, message="Comment not found"):
        super().__init__(message, status_code=404)


class CommentCreationFailedException(ApplicationException):
    """Exception raised when comment creation fails."""

    def __init__(self, message="Comment creation failed"):
        super().__init__(message, status_code=500)


class CommentUpdateFailedException(ApplicationException):
    """Exception raised when comment update fails."""

    def __init__(self, message="Comment update failed"):
        super().__init__(message, status_code=500)


class CommentDeletionFailedException(ApplicationException):
    """Exception raised when comment deletion fails."""

    def __init__(self, message="Comment deletion failed"):
        super().__init__(message, status_code=500)


class InvalidPasswordException(ApplicationException):
    """Exception raised when an invalid password is provided."""

    def __init__(self, message="Invalid password, password must be at least 8 characters long and contain at least one "
                               "uppercase letter, one lowercase letter, one number, and one special character"):
        super().__init__(message, status_code=400)


class InvalidEmailException(ApplicationException):
    """Exception raised when an invalid email is provided."""

    def __init__(self, message="Invalid email"):
        super().__init__(message, status_code=400)


class InvalidCredentialsException(ApplicationException):
    """Exception raised when invalid credentials are provided."""

    def __init__(self, message="Invalid credentials"):
        super().__init__(message, status_code=401)


class MailSendException(ApplicationException):
    """Exception raised when an error occurs while sending an email."""

    def __init__(self, message="Error occurred while sending email"):
        super().__init__(message, status_code=500)


class TokenExpiredException(ApplicationException):
    """Exception raised when a token has expired."""

    def __init__(self, message="Token has expired"):
        super().__init__(message, status_code=400)


class TokenInvalidException(ApplicationException):
    """Exception raised when a token is invalid."""

    def __init__(self, message="Token is invalid"):
        super().__init__(message, status_code=400)


class PostAlreadyLikedException(ApplicationException):
    """Exception raised when a post is already liked."""

    def __init__(self, message="Post already liked"):
        super().__init__(message, status_code=400)


class LikeNotFoundException(ApplicationException):
    """Exception raised when a like is not found."""

    def __init__(self, message="Like not found"):
        super().__init__(message, status_code=404)


class LikeAlreadyExistsException(ApplicationException):
    """Exception raised when a like already exists."""

    def __init__(self, message="You already liked this post"):
        super().__init__(message, status_code=400)


class FavoriteNotFoundException(ApplicationException):
    """Exception raised when a favorite is not found."""

    def __init__(self, message="Favorite not found"):
        super().__init__(message, status_code=404)


class FavoriteAlreadyExistsException(ApplicationException):
    """Exception raised when a favorite already exists."""

    def __init__(self, message="You already favorited this post"):
        super().__init__(message, status_code=400)


class FavoriteDeletionFailedException(ApplicationException):
    """Exception raised when favorite deletion fails."""

    def __init__(self, message="Favorite deletion failed"):
        super().__init__(message, status_code=500)


class AuthorizationException(ApplicationException):
    """Exception raised when a user is not authorized to perform an action."""

    def __init__(self, message="You are not authorized to perform this action"):
        super().__init__(message, status_code=403)


class UserUpdateFailedException(ApplicationException):
    """Exception raised when user update fails."""

    def __init__(self, message="User update failed"):
        super().__init__(message, status_code=500)


class UserDeletionFailedException(ApplicationException):
    """Exception raised when user deletion fails."""

    def __init__(self, message="User deletion failed"):
        super().__init__(message, status_code=500)


class FavoriteCreationFailedException(ApplicationException):
    """Exception raised when favorite creation fails."""

    def __init__(self, message="Favorite creation failed"):
        super().__init__(message, status_code=500)
