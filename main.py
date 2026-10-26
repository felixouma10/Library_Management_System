from services.auth_service import AuthService
from services.library_service import LibraryService
from utils.validators import validate_not_empty, get_menu_choice

def login_menu(auth_service):
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Login")
    print("2. Exit")

    choice = get_menu_choice(1, 2)

    if choice == 2:
        return False

    try:
        username = validate_not_empty(
            input("Enter username: "),
            "Username"
        )

        password = validate_not_empty(
            input("Enter password: "),
            "Password"
        )

        auth_service.login(username, password)

    except ValueError as error:
        print(f"\nError: {error}")

    return True

def student_menu(library_service, auth_service):
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
                search_term = validate_not_empty(
                    input("Enter title, author, or category: "),
                    "Search term"
                )
                library_service.search_books(search_term)

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
                search_term = validate_not_empty(
                    input("Enter title, author, or category: "),
                    "Search term"
                )
                library_service.search_books(search_term)

            elif choice == 3:
                book_id = validate_not_empty(
                    input("Enter new book ID: "),
                    "Book ID"
                )

                title = validate_not_empty(
                    input("Enter book title: "),
                    "Title"
                )

                author = validate_not_empty(
                    input("Enter author name: "),
                    "Author"
                )

                category = validate_not_empty(
                    input("Enter book category: "),
                    "Category"
                )

                library_service.add_book(
                    book_id,
                    title,
                    author,
                    category
                )

            elif choice == 4:
                book_id = validate_not_empty(
                    input("Enter book ID to remove: "),
                    "Book ID"
                )
                library_service.remove_book(book_id)

            elif choice == 5:
                library_service.view_borrowing_records()

            elif choice == 6:
                auth_service.logout()

        except ValueError as error:
            print(f"\nError: {error}")


def main():
    auth_service = AuthService()
    library_service = LibraryService(auth_service)

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


if __name__ == "__main__":
    main()