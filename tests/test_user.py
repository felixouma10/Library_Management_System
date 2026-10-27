
from models.user import User
from models.student import Student
from models.librarian import Librarian


def test_user_initial_values():
    user = User(
        "U001",
        "John Student",
        "john",
        "hashed_password",
        "student"
    )

    assert user.user_id == "U001"
    assert user.name == "John Student"
    assert user.username == "john"
    assert user.role == "student"


def test_user_password_check():
    user = User(
        "U001",
        "John Student",
        "john",
        "secret123",
        "student"
    )

    assert user.check_password("secret123") is True
    assert user.check_password("wrongpassword") is False


def test_user_to_dict():
    user = User(
        "U001",
        "John Student",
        "john",
        "hashed_password",
        "student"
    )

    data = user.to_dict()

    assert data == {
        "user_id": "U001",
        "name": "John Student",
        "username": "john",
        "password": "hashed_password",
        "role": "student"
    }


def test_user_string_representation():
    user = User(
        "U001",
        "John Student",
        "john",
        "hashed_password",
        "student"
    )

    result = str(user)

    assert "U001" in result
    assert "John Student" in result
    assert "Student" in result


def test_student_inherits_from_user():
    student = Student(
        "U001",
        "John Student",
        "john",
        "hashed_password"
    )

    assert isinstance(student, User)
    assert student.role == "student"
    assert student.name == "John Student"


def test_librarian_inherits_from_user():
    librarian = Librarian(
        "U002",
        "Jane Librarian",
        "jane",
        "hashed_password"
    )

    assert isinstance(librarian, User)
    assert librarian.role == "librarian"
    assert librarian.name == "Jane Librarian"


def test_user_properties_are_read_only():
    user = User(
        "U001",
        "John Student",
        "john",
        "hashed_password",
        "student"
    )

    try:
        user.name = "New Name"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "The name property should be read-only."
        )


def test_student_to_dict_preserves_role():
    student = Student(
        "U001",
        "John Student",
        "john",
        "hashed_password"
    )

    assert student.to_dict()["role"] == "student"


def test_librarian_to_dict_preserves_role():
    librarian = Librarian(
        "U002",
        "Jane Librarian",
        "jane",
        "hashed_password"
    )

    assert librarian.to_dict()["role"] == "librarian"
