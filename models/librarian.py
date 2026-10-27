from models.user import User


class Librarian(User):
    """Represent a librarian system user."""

    def __init__(
        self,
        user_id,
        name,
        username,
        password
    ):
        super().__init__(
            user_id,
            name,
            username,
            password,
            "librarian"
        )