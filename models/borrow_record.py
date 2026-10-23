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
        self.record_id = record_id
        self.student_id = student_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.status = status

    def return_book(self, return_date):
        self.return_date = return_date
        self.status = "returned"

    def to_dict(self):
        return {
            "record_id": self.record_id,
            "student_id": self.student_id,
            "book_id": self.book_id,
            "borrow_date": self.borrow_date,
            "return_date": self.return_date,
            "status": self.status
        }