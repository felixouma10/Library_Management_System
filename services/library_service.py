
from datetime import date

from models.book import Book
from models.borrow_record import BorrowRecord
from utils.json_manager import JSONManager
from utils.decorators import (
    login_required,
    role_required,
    log_action
)


class LibraryService:
    def __init__(self, auth_service):
        self.auth_service = auth_service
        self.books_file = "data/books.json"
        self.records_file = "data/borrow_records.json"

    @property
    def current_user(self):
        return self.auth_service.current_user

    def _load_books(self):
        books_data = JSONManager.load(self.books_file)
        return [
            Book(
                book["book_id"],
                book["title"],
                book["author"],
                book["category"],
                book.get("is_available", True)
            )
            for book in books_data
        ]

    def _save_books(self, books):
        JSONManager.save(
            self.books_file,
            [book.to_dict() for book in books]
        )

    def _load_records(self):
        records_data = JSONManager.load(self.records_file)
        return [
            BorrowRecord(
                record["record_id"],
                record["student_id"],
                record["book_id"],
                record["borrow_date"],
                record.get("return_date"),
                record.get("status", "borrowed")
            )
            for record in records_data
        ]

    def _save_records(self, records):
        JSONManager.save(
            self.records_file,
            [record.to_dict() for record in records]
        )

    @login_required
    def view_books(self):
        books = self._load_books()

        if not books:
            print("\nNo books found.")
            return

        print("\n--- LIBRARY CATALOGUE ---")

        for book in books:
            status = (
                "Available"
                if book.is_available
                else "Borrowed"
            )

            print(
                f"{book.book_id} | {book.title} | "
                f"{book.author} | {book.category} | {status}"
            )

    @login_required
    def search_books(self, search_term):
        books = self._load_books()
        search_term = search_term.strip().lower()

        matches = [
            book for book in books
            if search_term in book.title.lower()
            or search_term in book.author.lower()
            or search_term in book.category.lower()
        ]

        if not matches:
            print("\nNo matching books found.")
            return

        print("\n--- SEARCH RESULTS ---")

        for book in matches:
            status = (
                "Available"
                if book.is_available
                else "Borrowed"
            )

            print(
                f"{book.book_id} | {book.title} | "
                f"{book.author} | {book.category} | {status}"
            )

    @login_required
    @role_required("librarian")
    @log_action
    def add_book(self, book_id, title, author, category):
        books = self._load_books()

        if any(book.book_id == book_id for book in books):
            raise ValueError("A book with that ID already exists.")

        new_book = Book(book_id, title, author, category)
        books.append(new_book)
        self._save_books(books)

        print(f"\nBook '{title}' added successfully.")

    @login_required
    @role_required("librarian")
    @log_action
    def remove_book(self, book_id):
        books = self._load_books()

        book = next(
            (book for book in books if book.book_id == book_id),
            None
        )

        if book is None:
            raise ValueError("Book not found.")

        if not book.is_available:
            raise ValueError("Cannot remove a borrowed book.")

        books.remove(book)
        self._save_books(books)

        print("\nBook removed successfully.")

    @login_required
    @role_required("student")
    @log_action
    def borrow_book(self, book_id):
        books = self._load_books()

        book = next(
            (book for book in books if book.book_id == book_id),
            None
        )

        if book is None:
            raise ValueError("Book not found.")

        book.borrow()

        records = self._load_records()

        record_id = f"BR{len(records) + 1:03d}"

        record = BorrowRecord(
            record_id,
            self.current_user.user_id,
            book.book_id,
            date.today().isoformat()
        )

        records.append(record)

        self._save_books(books)
        self._save_records(records)

        print(f"\nYou have borrowed '{book.title}' successfully.")

    @login_required
    @role_required("student")
    @log_action
    def return_book(self, book_id):
        books = self._load_books()
        records = self._load_records()

        book = next(
            (book for book in books if book.book_id == book_id),
            None
        )

        if book is None:
            raise ValueError("Book not found.")

        record = next(
            (
                record for record in reversed(records)
                if record.book_id == book_id
                and record.student_id == self.current_user.user_id
                and record.status == "borrowed"
            ),
            None
        )

        if record is None:
            raise ValueError(
                "You do not have an active borrowing record for this book."
            )

        book.return_book()
        record.return_book(date.today().isoformat())

        self._save_books(books)
        self._save_records(records)

        print(f"\nYou have returned '{book.title}' successfully.")

    @login_required
    @role_required("student")
    def view_my_borrowing_records(self):
        records = self._load_records()

        my_records = [
            record for record in records
            if record.student_id == self.current_user.user_id
        ]

        if not my_records:
            print("\nYou have no borrowing records.")
            return

        print("\n--- MY BORROWING RECORDS ---")

        for record in my_records:
            print(
                f"Record: {record.record_id} | "
                f"Book ID: {record.book_id} | "
                f"Borrowed: {record.borrow_date} | "
                f"Returned: {record.return_date or 'Not returned'} | "
                f"Status: {record.status}"
            )

    @login_required
    @role_required("librarian")
    def view_borrowing_records(self):
        records = self._load_records()

        if not records:
            print("\nNo borrowing records found.")
            return

        print("\n--- ALL BORROWING RECORDS ---")

        for record in records:
            print(
                f"Record: {record.record_id} | "
                f"Student ID: {record.student_id} | "
                f"Book ID: {record.book_id} | "
                f"Borrowed: {record.borrow_date} | "
                f"Returned: {record.return_date or 'Not returned'} | "
                f"Status: {record.status}"
            )