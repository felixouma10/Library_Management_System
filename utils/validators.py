class User:
    def __init__(self, user_id, name, username, password, role):
        self._user_id = user_id
        self._name = name
        self._username = username
        self._password = password
        self._role = role

    @property
    def user_id(self):
        return self._user_id

    @property
    def name(self):
        return self._name

    @property
    def username(self):
        return self._username

    @property
    def role(self):
        return self._role

    def check_password(self, password):
        return self._password == password

    def to_dict(self):
        return {
            "user_id": self._user_id,
            "name": self._name,
            "username": self._username,
            "password": self._password,
            "role": self._role
        }

felix ouma
12:11 AM
import json
import os


class JSONManager:

    @staticmethod
    def load(filename):
        try:
            if not os.path.exists(filename):
                return []

            with open(filename, "r") as file:
                return json.load(file)

        except json.JSONDecodeError:
            print(f"Error: {filename} contains invalid JSON.")
            return []

        except OSError as error:
            print(f"Error reading {filename}: {error}")
            return []

    @staticmethod
    def save(filename, data):
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)

        except OSError as error:
            print(f"Error saving data: {error}")

felix ouma
12:17 AM
def validate_not_empty(value, field_name):
    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")

    return value.strip()


def get_menu_choice(minimum, maximum):
    while True:
        try:
            choice = int(input("Enter your choice: "))

            if minimum <= choice <= maximum:
                return choice

            print(
                f"Please enter a number between "
                f"{minimum} and {maximum}."
            )

        except ValueError:
            print("Invalid input. Please enter a number.")