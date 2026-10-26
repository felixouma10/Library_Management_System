class BorrowRecord:
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

    @property
    def record_id(self):
        return self._record_id

    @property
    def student_id(self):
        return self._student_id

    @property
    def book_id(self):
        return self._book_id

    @property
    def borrow_date(self):
        return self._borrow_date

    @property
    def return_date(self):
        return self._return_date

    @property
    def status(self):
        return self._status

    def return_book(self, return_date):
        if self._status == "returned":
            raise ValueError("This book has already been returned.")

        self._return_date = return_date
        self._status = "returned"

    def to_dict(self):
        return {
            "record_id": self._record_id,
            "student_id": self._student_id,
            "book_id": self._book_id,
            "borrow_date": self._borrow_date,
            "return_date": self._return_date,
            "status": self._status
        }