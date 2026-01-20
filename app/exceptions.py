class BackendException(Exception):
    """Base exception for the application"""
    pass

class UserAlreadyExistsError(BackendException):
    def __init__(self, email: str):
        self.message = f"User with email {email} already exists"
        super().__init__(self.message)

class UserNotFoundError(BackendException):
    def __init__(self, user_id: int = None, email: str = None):
        if user_id:
            self.message = f"User with id {user_id} not found"
        elif email:
            self.message = f"User with email {email} not found"
        else:
            self.message = "User not found"
        super().__init__(self.message)

class PostNotFoundError(BackendException):
    def __init__(self, post_id: int):
        self.message = f"Post with id {post_id} not found"
        super().__init__(self.message)

class AlreadyLikedError(BackendException):
    def __init__(self, post_id: int, user_id: int):
        self.message = f"User {user_id} already liked post {post_id}"
        super().__init__(self.message)

class NotLikedError(BackendException):
    def __init__(self, post_id: int, user_id: int):
        self.message = f"User {user_id} has not liked post {post_id}"
        super().__init__(self.message)
