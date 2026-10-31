import json
import pytest
from services.auth_service import AuthService

@pytest.fixture
def auth_service(tmp_path):
    service = AuthService()
    service.users_file = str(tmp_path / "users.json")

    with open(service.users_file, "w", encoding="utf-8") as file:
        json.dump([], file)

    return service

def test_password_is_hashed():
    hashed = AuthService.hash_password("secret123")

    assert hashed != "secret123"
    assert hashed.startswith("$2b$")
    assert AuthService.verify_password("secret123", hashed)


def test_same_password_produces_different_hashes():
    first_hash = AuthService.hash_password("secret123")
    second_hash = AuthService.hash_password("secret123")

    assert first_hash != second_hash

    assert AuthService.verify_password("secret123", first_hash)
    assert AuthService.verify_password("secret123", second_hash)


def test_registration_saves_bcrypt_hashed_password(auth_service):
    auth_service.register_student(
        "John Student", "john", "secret123"
    )

    with open(auth_service.users_file, "r", encoding="utf-8") as file:
        users = json.load(file)

    assert len(users) == 1
    assert users[0]["username"] == "john"
    assert users[0]["role"] == "student"
    assert users[0]["password"].startswith("$2b$")
    assert AuthService.verify_password(
        "secret123", users[0]["password"]
    )


def test_registration_saves_hashed_password(auth_service):
    auth_service.register_student(
        "John Student", "john", "secret123"
    )

    with open(auth_service.users_file, "r", encoding="utf-8") as file:
        users = json.load(file)

    assert len(users) == 1
    assert users[0]["username"] == "john"
    assert users[0]["role"] == "student"
    assert users[0]["password"].startswith("$2b$")
    assert AuthService.verify_password(
    "secret123", users[0]["password"])

def test_duplicate_username_is_rejected(auth_service):
    auth_service.register_student(
        "John Student", "john", "secret123"
    )

    with pytest.raises(ValueError, match="already exists"):
        auth_service.register_student(
            "Another Student", "JOHN", "another123"
        )


def test_successful_login(auth_service, capsys):
    auth_service.register_student(
        "John Student", "john", "secret123"
    )

    user = auth_service.login("john", "secret123")

    assert user is not None
    assert user.username == "john"
    assert user.role == "student"
    assert auth_service.current_user is user


def test_login_is_case_insensitive_for_username(auth_service, capsys):
    auth_service.register_student(
        "John Student", "john", "secret123"
    )

    user = auth_service.login("JOHN", "secret123")

    assert user is not None
    assert user.username == "john"


def test_incorrect_password_is_rejected(auth_service, capsys):
    auth_service.register_student(
        "John Student", "john", "secret123"
    )

    user = auth_service.login("john", "wrongpassword")

    assert user is None
    assert auth_service.current_user is None


def test_unknown_username_is_rejected(auth_service, capsys):
    user = auth_service.login("unknown", "secret123")

    assert user is None
    assert auth_service.current_user is None


def test_logout_clears_current_user(auth_service, capsys):
    auth_service.register_student(
        "John Student", "john", "secret123"
    )
    auth_service.login("john", "secret123")

    auth_service.logout()

    assert auth_service.current_user is None


def test_legacy_password_is_upgraded(auth_service, capsys):
    legacy_user = [{
        "user_id": "U005",
        "name": "Legacy Student",
        "username": "legacy",
        "password": "oldpassword",
        "role": "student"
    }]

    with open(auth_service.users_file, "w", encoding="utf-8") as file:
        json.dump(legacy_user, file)

    user = auth_service.login("legacy", "oldpassword")

    assert user is not None

    with open(auth_service.users_file, "r", encoding="utf-8") as file:
        saved_users = json.load(file)

    upgraded_password = saved_users[0]["password"]

    assert upgraded_password.startswith("$2b$")
    assert AuthService.verify_password(
        "oldpassword", upgraded_password
    )
