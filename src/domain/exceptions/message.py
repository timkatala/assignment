class MessageNotFoundException(Exception):
    """Exception raised when a message with given id doesn't exist"""

    def __init__(self, message="Message doesn't exist"):
        self.message = message
        super().__init__(self.message)
