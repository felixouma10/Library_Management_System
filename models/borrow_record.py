class BorrowRecord:
    """Represent a book borrowing transaction."""

    total_records = 0

    def __init__(
        self,
        record_id,
        student_id,
        book_id,
        borrow_date,
        return_date=None,
        status="borrowed"
    ):
        self._record_id = record_id
        self._student_id = student_id
        self._book_id = book_id
        self._borrow_date = borrow_date
        self._return_date = return_date
        self._status = status

        BorrowRecord.total_records += 1

    @property
    def record_id(self):
        """Return the borrowing record ID."""

        return self._record_id

    @property
    def student_id(self):
        """Return the student ID."""

        return self._student_id

    @property
    def book_id(self):
        """Return the book ID."""

        return self._book_id

    @property
    def borrow_date(self):
        """Return the borrowing date."""

        return self._borrow_date

    @property
    def return_date(self):
        """Return the return date."""

        return self._return_date

    @property
    def status(self):
        """Return the current record status."""

        return self._status

    def return_book(self, return_date):
        """Mark the borrowing record as returned."""

        if self._status == "returned":

            raise ValueError(
                "This book has already been returned."
            )

        self._return_date = return_date
        self._status = "returned"

    def to_dict(self):
        """Convert the borrowing record to a dictionary."""

        return {
            "record_id": self._record_id,
            "student_id": self._student_id,
            "book_id": self._book_id,
            "borrow_date": self._borrow_date,
            "return_date": self._return_date,
            "status": self._status
        }

    @classmethod
    def from_dict(cls, data):
        """Create a BorrowRecord from dictionary data."""

        return cls(
            data["record_id"],
            data["student_id"],
            data["book_id"],
            data["borrow_date"],
            data.get("return_date"),
            data.get("status", "borrowed")
        )

    def __str__(self):
        """Return a readable representation of the record."""

        return (
            f"{self._record_id} | "
            f"Student: {self._student_id} | "
            f"Book: {self._book_id} | "
            f"Status: {self._status}"
        )