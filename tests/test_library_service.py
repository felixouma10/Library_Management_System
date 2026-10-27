
import json

import pytest

from services.auth_service import AuthService
from services.library_service import LibraryService


@pytest.fixture
def library_setup(tmp_path):
    """Create an isolated library with sample users and books."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    users_file = data_dir / "users.json"
    books_file = data_dir / "books.json"
    records_file = data_dir / "borrow_records.json"

    users = [
        {
            "user_id": "U001",
            "name": "John Student",
            "username": "john",
            "password": AuthService.hash_password("secret123"),
            "role": "student"
        },
        {
            "user_id": "U002",
            "name": "Jane Librarian",
            "username": "jane",
            "password": AuthService.hash_password("admin123"),
            "role": "librarian"
        }
    ]

    books = [
        {
            "book_id": "B001",
            "title": "Python Programming",
            "author": "Mark Smith",
            "category": "Programming",
            "is_available": True
        },
        {
            "book_id": "B002",
            "title": "Database Systems",
            "author": "Jane Brown",
            "category": "Technology",
            "is_available": True
        }
    ]

    users_file.write_text(json.dumps(users), encoding="utf-8")
    books_file.write_text(json.dumps(books), encoding="utf-8")
    records_file.write_text("[]", encoding="utf-8")

    auth = AuthService()
    auth.users_file = str(users_file)

    library = LibraryService(auth)
    library.books_file = str(books_file)
    library.records_file = str(records_file)

    return library, auth, books_file, records_file


def test_student_can_view_books(library_setup, capsys):
    library, auth, _, _ = library_setup
    auth.login("john", "secret123")

    library.view_books()

    output = capsys.readouterr().out
    assert "Python Programming" in output
    assert "Database Systems" in output


def test_student_can_search_books(library_setup, capsys):
    library, auth, _, _ = library_setup
    auth.login("john", "secret123")

    library.search_books("python")

    output = capsys.readouterr().out
    assert "Python Programming" in output
    assert "Database Systems" not in output


def test_librarian_can_add_book(library_setup):
    library, auth, books_file, _ = library_setup
    auth.login("jane", "admin123")

    library.add_book(
        "B003",
        "Software Engineering",
        "Mary Jones",
        "Technology"
    )

    books = json.loads(books_file.read_text(encoding="utf-8"))

    assert len(books) == 3
    assert books[-1]["book_id"] == "B003"


def test_librarian_cannot_add_duplicate_book_id(library_setup):
    library, auth, _, _ = library_setup
    auth.login("jane", "admin123")

    with pytest.raises(ValueError, match="already exists"):
        library.add_book(
            "B001",
            "Another Book",
            "Another Author",
            "Technology"
        )


def test_librarian_can_remove_available_book(library_setup):
    library, auth, books_file, _ = library_setup
    auth.login("jane", "admin123")

    library.remove_book("B001")

    books = json.loads(books_file.read_text(encoding="utf-8"))

    assert len(books) == 1
    assert books[0]["book_id"] == "B002"


def test_student_can_borrow_book(library_setup):
    library, auth, books_file, records_file = library_setup
    auth.login("john", "secret123")

    library.borrow_book("B001")

    books = json.loads(books_file.read_text(encoding="utf-8"))
    records = json.loads(records_file.read_text(encoding="utf-8"))

    assert books[0]["is_available"] is False
    assert len(records) == 1
    assert records[0]["student_id"] == "U001"
    assert records[0]["book_id"] == "B001"
    assert records[0]["status"] == "borrowed"


def test_student_cannot_borrow_same_book_twice(library_setup):
    library, auth, _, _ = library_setup
    auth.login("john", "secret123")

    library.borrow_book("B001")

    with pytest.raises(ValueError, match="already borrowed"):
        library.borrow_book("B001")


def test_student_can_return_borrowed_book(library_setup):
    library, auth, books_file, records_file = library_setup
    auth.login("john", "secret123")

    library.borrow_book("B001")
    library.return_book("B001")

    books = json.loads(books_file.read_text(encoding="utf-8"))
    records = json.loads(records_file.read_text(encoding="utf-8"))

    assert books[0]["is_available"] is True
    assert records[0]["status"] == "returned"
    assert records[0]["return_date"] is not None


def test_student_cannot_return_book_not_borrowed(library_setup):
    library, auth, _, _ = library_setup
    auth.login("john", "secret123")

    with pytest.raises(ValueError, match="active borrowing record"):
        library.return_book("B001")


def test_student_cannot_add_books(library_setup, capsys):
    library, auth, books_file, _ = library_setup
    auth.login("john", "secret123")

    library.add_book(
        "B003",
        "Software Engineering",
        "Mary Jones",
        "Technology"
    )

    output = capsys.readouterr().out
    books = json.loads(books_file.read_text(encoding="utf-8"))

    assert "Access denied" in output
    assert len(books) == 2


def test_librarian_cannot_borrow_books(library_setup, capsys):
    library, auth, books_file, _ = library_setup
    auth.login("jane", "admin123")

    library.borrow_book("B001")

    output = capsys.readouterr().out
    books = json.loads(books_file.read_text(encoding="utf-8"))

    assert "Access denied" in output
    assert books[0]["is_available"] is True


def test_unauthenticated_user_cannot_view_books(
    library_setup, capsys
):
    library, _, _, _ = library_setup

    library.view_books()

    assert "Please login first" in capsys.readouterr().out
