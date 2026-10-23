from models.user import User


class Student(User):
    def __init__(self, user_id, name, username, password):
        super().__init__(
            user_id,
            name,
            username,
            password,
            "student"
        )