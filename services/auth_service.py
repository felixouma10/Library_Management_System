import hashlib
import bcrypt

from models.student import Student
from models.librarian import Librarian
from utils.json_manager import JSONManager


class AuthService:
    """Handle registration, authentication and logout."""

    def __init__(self):
        self.current_user = None
        self.users_file = "data/users.json"

    @staticmethod
    def _bcrypt_password(password):
        """Prepare passwords for bcrypt, including passwords over 72 bytes."""
        password_bytes = password.encode("utf-8")
        return hashlib.sha256(
            b"LibraryManagementSystem\x00" + password_bytes
        ).hexdigest().encode("utf-8")

    @staticmethod
    def hash_password(password):
        """Return a salted bcrypt password hash."""
        password_bytes = AuthService._bcrypt_password(password)

        return bcrypt.hashpw(
            password_bytes,
            bcrypt.gensalt()
        ).decode("utf-8")

    @staticmethod
    def verify_password(password, stored_password):
        """Verify bcrypt and support legacy SHA-256/plain-text passwords."""
        if stored_password.startswith(("$2a$", "$2b$", "$2y$")):
            try:
                return bcrypt.checkpw(
                    AuthService._bcrypt_password(password),
                    stored_password.encode("utf-8")
                )
            except (ValueError, TypeError):
                return False

        # Support existing SHA-256 passwords during migration.
        sha256_password = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

        if stored_password == sha256_password:
            return True

        # Support older plain-text passwords during migration.
        return stored_password == password

    def login(self, username, password):
        """Authenticate a user and upgrade legacy passwords."""
        users = JSONManager.load(self.users_file)

        for user_data in users:
            stored_username = user_data.get("username", "")

            if stored_username.lower() != username.lower():
                continue

            stored_password = user_data.get("password", "")

            if not self.verify_password(password, stored_password):
                break

            # Upgrade SHA-256 and plain-text passwords to bcrypt.
            if not stored_password.startswith(("$2a$", "$2b$", "$2y$")):
                user_data["password"] = self.hash_password(password)
                JSONManager.save(self.users_file, users)

            role = user_data.get("role", "").lower()
            user_id = user_data.get("user_id")
            name = user_data.get("name", "")
            hashed_password = user_data["password"]

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
