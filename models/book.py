class Book:
    """Represent a book in the library."""

    total_books = 0

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

        Book.total_books += 1

    @property
    def book_id(self):
        """Return the book ID."""

        return self._book_id

    @property
    def title(self):
        """Return the book title."""

        return self._title

    @title.setter
    def title(self, value):
        """Update the book title."""

        if not value.strip():
            raise ValueError(
                "Book title cannot be empty."
            )

        self._title = value.strip()

    @property
    def author(self):
        """Return the book author."""

        return self._author

    @author.setter
    def author(self, value):
        """Update the book author."""

        if not value.strip():
            raise ValueError(
                "Author cannot be empty."
            )

        self._author = value.strip()

    @property
    def category(self):
        """Return the book category."""

        return self._category

    @category.setter
    def category(self, value):
        """Update the book category."""

        if not value.strip():
            raise ValueError(
                "Category cannot be empty."
            )

        self._category = value.strip()

    @property
    def is_available(self):
        """Return whether the book is available."""

        return self._is_available

    def borrow(self):
        """Mark the book as borrowed."""

        if not self._is_available:
            raise ValueError(
                "Book is already borrowed."
            )

        self._is_available = False

    def return_book(self):
        """Mark the book as available."""

        if self._is_available:
            raise ValueError(
                "Book is already available."
            )

        self._is_available = True

    def to_dict(self):
        """Convert the book object into a dictionary."""

        return {
            "book_id": self._book_id,
            "title": self._title,
            "author": self._author,
            "category": self._category,
            "is_available": self._is_available
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Book object from dictionary data."""

        return cls(
            data["book_id"],
            data["title"],
            data["author"],
            data["category"],
            data.get("is_available", True)
        )

    def __str__(self):
        """Return a readable representation of the book."""

        status = (
            "Available"
            if self._is_available
            else "Borrowed"
        )

        return (
            f"{self._book_id} | "
            f"{self._title} | "
            f"{self._author} | "
            f"{self._category} | "
            f"{status}"
        )