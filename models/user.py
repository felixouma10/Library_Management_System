class User:
    """Base class representing a system user."""

    def __init__(
        self,
        user_id,
        name,
        username,
        password,
        role
    ):
        self._user_id = user_id
        self._name = name
        self._username = username
        self._password = password
        self._role = role

    @property
    def user_id(self):
        """Return the user's ID."""

        return self._user_id

    @property
    def name(self):
        """Return the user's name."""

        return self._name

    @property
    def username(self):
        """Return the user's username."""

        return self._username

    @property
    def role(self):
        """Return the user's role."""

        return self._role

    def check_password(self, password):
        """Check whether a password matches the stored password."""

        return self._password == password

    def to_dict(self):
        """Convert the user object into a dictionary."""

        return {
            "user_id": self._user_id,
            "name": self._name,
            "username": self._username,
            "password": self._password,
            "role": self._role
        }

    def __str__(self):
        """Return a readable representation of the user."""

        return (
            f"{self._user_id} - "
            f"{self._name} - "
            f"{self._role.title()}"
        )