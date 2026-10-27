
import pytest

from models.borrow_record import BorrowRecord


@pytest.fixture
def borrow_record():
    """Create a sample borrowing record."""
    return BorrowRecord(
        "BR001",
        "U001",
        "B001",
        "2026-10-01"
    )


def test_borrow_record_initial_values(borrow_record):
    assert borrow_record.record_id == "BR001"
    assert borrow_record.student_id == "U001"
    assert borrow_record.book_id == "B001"
    assert borrow_record.borrow_date == "2026-10-01"
    assert borrow_record.return_date is None
    assert borrow_record.status == "borrowed"


def test_borrow_record_can_be_returned(borrow_record):
    borrow_record.return_book("2026-10-05")

    assert borrow_record.return_date == "2026-10-05"
    assert borrow_record.status == "returned"


def test_cannot_return_record_twice(borrow_record):
    borrow_record.return_book("2026-10-05")

    with pytest.raises(
        ValueError,
        match="already been returned"
    ):
        borrow_record.return_book("2026-10-06")


def test_borrow_record_to_dict(borrow_record):
    data = borrow_record.to_dict()

    assert data == {
        "record_id": "BR001",
        "student_id": "U001",
        "book_id": "B001",
        "borrow_date": "2026-10-01",
        "return_date": None,
        "status": "borrowed"
    }


def test_borrow_record_from_dict():
    data = {
        "record_id": "BR002",
        "student_id": "U002",
        "book_id": "B003",
        "borrow_date": "2026-10-01",
        "return_date": "2026-10-03",
        "status": "returned"
    }

    record = BorrowRecord.from_dict(data)

    assert record.record_id == "BR002"
    assert record.student_id == "U002"
    assert record.book_id == "B003"
    assert record.return_date == "2026-10-03"
    assert record.status == "returned"


def test_borrow_record_string_representation(borrow_record):
    result = str(borrow_record)

    assert "BR001" in result
    assert "U001" in result
    assert "B001" in result
    assert "borrowed" in result
