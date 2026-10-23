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