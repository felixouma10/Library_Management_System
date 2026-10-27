
import argparse
from getpass import getpass

from services.auth_service import AuthService
from services.library_service import LibraryService

from utils.validators import (
    validate_not_empty,
    validate_password,
    get_menu_choice
)


def register_menu(auth_service):
    """Register a new student interactively."""
    print("\n===== STUDENT REGISTRATION =====")

    try:
        name = validate_not_empty(
            input("Enter your name: "), "Name"
        )
        username = validate_not_empty(
            input("Enter username: "), "Username"
        )
        password = validate_password(
            getpass("Enter password: ")
        )
        confirm_password = getpass("Confirm password: ")

        if password != confirm_password:
            raise ValueError("Passwords do not match.")

        auth_service.register_student(name, username, password)

    except ValueError as error:
        print(f"\nError: {error}")


def login_menu(auth_service):
    """Display the interactive login and registration menu."""
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Login")
    print("2. Register")
    print("3. Exit")

    choice = get_menu_choice(1, 3)

    if choice == 3:
        return False

    if choice == 2:
        register_menu(auth_service)
        return True

    try:
        username = validate_not_empty(
            input("Enter username: "), "Username"
        )
        password = getpass("Enter password: ")
        validate_not_empty(password, "Password")
        auth_service.login(username, password)

    except ValueError as error:
        print(f"\nError: {error}")

    return True


def student_menu(library_service, auth_service):
    """Display the student menu."""
    while auth_service.current_user is not None:
        print("\n===== STUDENT MENU =====")
        print("1. View all books")
        print("2. Search books")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. View my borrowing records")
        print("6. Logout")

        choice = get_menu_choice(1, 6)

        try:
            if choice == 1:
                library_service.view_books()

            elif choice == 2:
                term = validate_not_empty(
                    input("Enter title, author, or category: "),
                    "Search term"
                )
                library_service.search_books(term)

            elif choice == 3:
                book_id = validate_not_empty(
                    input("Enter book ID to borrow: "),
                    "Book ID"
                )
                library_service.borrow_book(book_id)

            elif choice == 4:
                book_id = validate_not_empty(
                    input("Enter book ID to return: "),
                    "Book ID"
                )
                library_service.return_book(book_id)

            elif choice == 5:
                library_service.view_my_borrowing_records()

            elif choice == 6:
                auth_service.logout()

        except ValueError as error:
            print(f"\nError: {error}")


def librarian_menu(library_service, auth_service):
    """Display the librarian menu."""
    while auth_service.current_user is not None:
        print("\n===== LIBRARIAN MENU =====")
        print("1. View all books")
        print("2. Search books")
        print("3. Add a book")
        print("4. Remove a book")
        print("5. View all borrowing records")
        print("6. Logout")

        choice = get_menu_choice(1, 6)

        try:
            if choice == 1:
                library_service.view_books()

            elif choice == 2:
                term = validate_not_empty(
                    input("Enter title, author, or category: "),
                    "Search term"
                )
                library_service.search_books(term)

            elif choice == 3:
                book_id = validate_not_empty(
                    input("Enter new book ID: "), "Book ID"
                )
                title = validate_not_empty(
                    input("Enter book title: "), "Title"
                )
                author = validate_not_empty(
                    input("Enter author name: "), "Author"
                )
                category = validate_not_empty(
                    input("Enter book category: "), "Category"
                )

                library_service.add_book(
                    book_id, title, author, category
                )

            elif choice == 4:
                book_id = validate_not_empty(
                    input("Enter book ID to remove: "), "Book ID"
                )
                library_service.remove_book(book_id)

            elif choice == 5:
                library_service.view_borrowing_records()

            elif choice == 6:
                auth_service.logout()

        except ValueError as error:
            print(f"\nError: {error}")


def run_interactive(auth_service, library_service):
    """Run the original menu-driven application."""
    while True:
        if auth_service.current_user is None:
            if not login_menu(auth_service):
                print("\nThank you for using the Library Management System.")
                break
            continue

        role = auth_service.current_user.role

        if role == "student":
            student_menu(library_service, auth_service)
        elif role == "librarian":
            librarian_menu(library_service, auth_service)
        else:
            print("\nUnknown user role.")
            auth_service.logout()


def authenticate_cli(auth_service, username=None):
    """Authenticate a user for a single CLI command."""
    if username is None:
        username = input("Username: ")

    username = validate_not_empty(username, "Username")
    password = getpass("Password: ")

    validate_not_empty(password, "Password")

    return auth_service.login(username, password) is not None


def build_parser():
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Library Management System CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        help="Available operations"
    )

    subparsers.add_parser(
        "interactive",
        help="Open the interactive menu"
    )

    subparsers.add_parser(
        "register",
        help="Register a new student account"
    )

    login_parser = subparsers.add_parser(
        "login",
        help="Authenticate a user"
    )
    login_parser.add_argument(
        "--username",
        help="Username (password will be prompted securely)"
    )

    books_parser = subparsers.add_parser(
        "books",
        help="Display the library catalogue"
    )
    books_parser.add_argument("--username")

    search_parser = subparsers.add_parser(
        "search",
        help="Search the library catalogue"
    )
    search_parser.add_argument(
        "--term",
        required=True,
        help="Book title, author, or category"
    )
    search_parser.add_argument("--username")

    borrow_parser = subparsers.add_parser(
        "borrow",
        help="Borrow a book as a student"
    )
    borrow_parser.add_argument(
        "--book-id",
        required=True,
        help="ID of the book to borrow"
    )
    borrow_parser.add_argument("--username")

    return_parser = subparsers.add_parser(
        "return",
        help="Return a borrowed book as a student"
    )
    return_parser.add_argument(
        "--book-id",
        required=True,
        help="ID of the book to return"
    )
    return_parser.add_argument("--username")

    records_parser = subparsers.add_parser(
        "records",
        help="View borrowing records for your role"
    )
    records_parser.add_argument("--username")

    return parser


def main():
    """Start the application or execute a CLI command."""
    parser = build_parser()
    args = parser.parse_args()

    auth_service = AuthService()
    library_service = LibraryService(auth_service)

    # No subcommand means start the interactive application.
    if args.command is None or args.command == "interactive":
        run_interactive(auth_service, library_service)
        return

    try:
        if args.command == "register":
            register_menu(auth_service)
            return

        if args.command == "login":
            authenticate_cli(auth_service, args.username)
            return

        # All remaining commands require authentication.
        if not authenticate_cli(
            auth_service,
            getattr(args, "username", None)
        ):
            return

        if args.command == "books":
            library_service.view_books()

        elif args.command == "search":
            term = validate_not_empty(args.term, "Search term")
            library_service.search_books(term)

        elif args.command == "borrow":
            library_service.borrow_book(args.book_id)

        elif args.command == "return":
            library_service.return_book(args.book_id)

        elif args.command == "records":
            role = auth_service.current_user.role

            if role == "student":
                library_service.view_my_borrowing_records()
            elif role == "librarian":
                library_service.view_borrowing_records()
            else:
                print("\nUnknown user role.")

    except ValueError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
