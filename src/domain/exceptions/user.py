class UserAlreadyExistsException(Exception):
    """Exception raised when a user with the same email already exists."""

    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    """Exception raised when a user with given id doesn't exist"""

    def __init__(self, message="User doesn't exist"):
        self.message = message
        super().__init__(self.message)
