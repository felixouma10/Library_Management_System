
import hashlib

from models.student import Student
from models.librarian import Librarian
from utils.json_manager import JSONManager


class AuthService:
    """Handle registration, authentication and logout."""

    def __init__(self):
        self.current_user = None
        self.users_file = "data/users.json"

    @staticmethod
    def hash_password(password):
        """Return a SHA-256 hash of a password."""
        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    def login(self, username, password):
        """Authenticate a user and upgrade legacy passwords."""
        users = JSONManager.load(self.users_file)
        hashed_password = self.hash_password(password)

        for user_data in users:
            stored_username = user_data.get("username", "")

            if stored_username.lower() != username.lower():
                continue

            stored_password = user_data.get("password", "")

            # Support existing hashed and legacy plain-text passwords.
            if stored_password == hashed_password:
                password_matches = True
            elif stored_password == password:
                password_matches = True

                # Upgrade the legacy password after successful login.
                user_data["password"] = hashed_password
                JSONManager.save(self.users_file, users)
            else:
                password_matches = False

            if not password_matches:
                break

            role = user_data.get("role", "").lower()
            user_id = user_data.get("user_id")
            name = user_data.get("name", "")

            if role == "student":
                self.current_user = Student(
                    user_id, name, stored_username, hashed_password
                )
            elif role == "librarian":
                self.current_user = Librarian(
                    user_id, name, stored_username, hashed_password
                )
            else:
                print("\nInvalid user role.")
                return None

            print(f"\nWelcome, {self.current_user.name}!")
            return self.current_user

        print("\nInvalid username or password.")
        return None

    def register_student(self, name, username, password):
        """Register a student with a unique username."""
        users = JSONManager.load(self.users_file)

        for user in users:
            if user.get("username", "").lower() == username.lower():
                raise ValueError("Username already exists.")

        user_id = self._generate_user_id(users)
        hashed_password = self.hash_password(password)

        student = Student(
            user_id,
            name,
            username,
            hashed_password
        )

        users.append(student.to_dict())
        JSONManager.save(self.users_file, users)

        print("\nStudent registration successful.")
        print(f"Your user ID is: {user_id}")
        return student

    @staticmethod
    def _generate_user_id(users):
        """Generate the next available student/user ID."""
        highest_number = 0

        for user in users:
            user_id = user.get("user_id", "")

            if user_id.startswith("U"):
                try:
                    number = int(user_id[1:])
                    highest_number = max(highest_number, number)
                except ValueError:
                    continue

        return f"U{highest_number + 1:03d}"

    def logout(self):
        """End the current user's session."""
        if self.current_user is None:
            print("\nNo user is currently logged in.")
            return

        print(f"\nGoodbye, {self.current_user.name}!")
        self.current_user = None
