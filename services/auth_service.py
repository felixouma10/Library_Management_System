
from models.student import Student
from models.librarian import Librarian
from utils.json_manager import JSONManager


class AuthService:
    def __init__(self):
        self.current_user = None
        self.users_file = "data/users.json"

    def login(self, username, password):
        users = JSONManager.load(self.users_file)

        for user_data in users:
            if user_data["username"] == username:
                if user_data["password"] == password:

                    role = user_data["role"].lower()

                    if role == "student":
                        self.current_user = Student(
                            user_data["user_id"],
                            user_data["name"],
                            user_data["username"],
                            user_data["password"]
                        )

                    elif role == "librarian":
                        self.current_user = Librarian(
                            user_data["user_id"],
                            user_data["name"],
                            user_data["username"],
                            user_data["password"]
                        )

                    else:
                        print("Invalid user role.")
                        return None

                    print(
                        f"\nWelcome, "
                        f"{self.current_user.name}!"
                    )
                    return self.current_user

        print("\nInvalid username or password.")
        return None

    def logout(self):
        if self.current_user is None:
            print("\nNo user is currently logged in.")
            return

        print(
            f"\nGoodbye, "
            f"{self.current_user.name}!"
        )

        self.current_user = None
