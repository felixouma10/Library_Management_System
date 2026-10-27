
import pytest

from models.book import Book


@pytest.fixture
def book():
    """Create a sample book for testing."""
    return Book(
        "B001",
        "Python Programming",
        "Mark Smith",
        "Programming"
    )


def test_book_initial_values(book):
    assert book.book_id == "B001"
    assert book.title == "Python Programming"
    assert book.author == "Mark Smith"
    assert book.category == "Programming"
    assert book.is_available is True


def test_book_can_be_borrowed(book):
    book.borrow()

    assert book.is_available is False


def test_cannot_borrow_book_twice(book):
    book.borrow()

    with pytest.raises(ValueError, match="already borrowed"):
        book.borrow()


def test_book_can_be_returned(book):
    book.borrow()
    book.return_book()

    assert book.is_available is True


def test_cannot_return_available_book(book):
    with pytest.raises(ValueError, match="already available"):
        book.return_book()


def test_book_title_can_be_updated(book):
    book.title = "Advanced Python"

    assert book.title == "Advanced Python"


def test_book_rejects_empty_title(book):
    with pytest.raises(ValueError, match="cannot be empty"):
        book.title = "   "


def test_book_author_can_be_updated(book):
    book.author = "Jane Brown"

    assert book.author == "Jane Brown"


def test_book_rejects_empty_author(book):
    with pytest.raises(ValueError, match="cannot be empty"):
        book.author = ""


def test_book_category_can_be_updated(book):
    book.category = "Technology"

    assert book.category == "Technology"


def test_book_rejects_empty_category(book):
    with pytest.raises(ValueError, match="cannot be empty"):
        book.category = "   "


def test_book_to_dict(book):
    data = book.to_dict()

    assert data == {
        "book_id": "B001",
        "title": "Python Programming",
        "author": "Mark Smith",
        "category": "Programming",
        "is_available": True
    }


def test_book_from_dict():
    data = {
        "book_id": "B002",
        "title": "Database Systems",
        "author": "Jane Brown",
        "category": "Technology",
        "is_available": False
    }

    book = Book.from_dict(data)

    assert book.book_id == "B002"
    assert book.title == "Database Systems"
    assert book.is_available is False


def test_book_string_representation(book):
    result = str(book)

    assert "B001" in result
    assert "Python Programming" in result
    assert "Available" in result
