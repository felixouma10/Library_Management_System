class Book:
    def __init__(
        self,
        book_id,
        title,
        author,
        category,
        is_available=True
    ):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._category = category
        self._is_available = is_available

    @property
    def book_id(self):
        return self._book_id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def category(self):
        return self._category

    @property
    def is_available(self):
        return self._is_available

    def borrow(self):
        if not self._is_available:
            raise ValueError("Book is already borrowed.")

        self._is_available = False

    def return_book(self):
        if self._is_available:
            raise ValueError("Book is already available.")

        self._is_available = True

    def to_dict(self):
        return {
            "book_id": self._book_id,
            "title": self._title,
            "author": self._author,
            "category": self._category,
            "is_available": self._is_available
        }