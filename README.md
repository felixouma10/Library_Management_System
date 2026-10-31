# Library Management System

A Python command-line Library Management System built using Object-Oriented Programming (OOP).

The system allows students to register, log in, browse, search, borrow, and return books, while librarians can manage the book catalogue and monitor borrowing records.

The project demonstrates Object-Oriented Programming, inheritance, encapsulation, decorators, authentication, role-based authorization, JSON file persistence, input validation, exception handling, logging, command-line interfaces, automated testing, and Git/GitHub workflow.

---

## Features

### Student Features

- Register a student account.
- Log in and log out.
- View the library catalogue.
- Search for books by title, author, or category.
- Borrow available books.
- Return borrowed books.
- View personal borrowing records.
- Receive validation and error messages for invalid operations.

### Librarian Features

- Log in and log out.
- View the library catalogue.
- Search for books.
- Add new books.
- Remove available books.
- View all borrowing records.
- Access librarian-only operations through role-based authorization.

### System Features

- Object-Oriented Programming.
- Inheritance using `User`, `Student`, and `Librarian`.
- Encapsulation using properties and validation.
- Role-based access control.
- Password hashing.
- JSON-based data persistence.
- Command-line interface using `argparse`.
- Interactive menu-based interface.
- Input validation.
- Exception and file-error handling.
- Reusable decorators.
- Activity logging.
- Automated unit and CLI testing.
- Modular project structure.
- Git and GitHub version control.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Application development |
| `argparse` | Command-line argument parsing |
| JSON | Persistent data storage |
| `pytest` | Automated testing |
| Git | Version control |
| GitHub | Repository hosting and collaboration |

---

## Project Structure

```text
Library_Management_System/
│
├── main.py
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── student.py
│   ├── librarian.py
│   ├── book.py
│   └── borrow_record.py
│
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   └── library_service.py
│
├── utils/
│   ├── __init__.py
│   ├── decorators.py
│   ├── validators.py
│   └── json_manager.py
│
├── data/
│   ├── users.json
│   ├── books.json
│   └── borrow_records.json
│
├── logs/
│   └── library.log
│
├── tests/
│   ├── __init__.py
│   ├── test_auth_service.py
│   ├── test_book.py
│   ├── test_borrow_record.py
│   ├── test_cli.py
│   ├── test_json_manager.py
│   ├── test_library_service.py
│   ├── test_user.py
│   └── test_validators.py
│
├── requirements.txt
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── README.md
```

---

# Object-Oriented Design

The application uses classes to model users, books, and borrowing records.

## Main Classes

### `User`

`User` is the base class for users of the system.

It contains shared user information and functionality such as:

- User ID
- Username
- Password
- Role
- Password verification
- Serialization and deserialization

### `Student`

`Student` inherits from `User` and represents a student account.

Students can:

- View books
- Search books
- Borrow books
- Return books
- View their borrowing records

### `Librarian`

`Librarian` inherits from `User` and represents a librarian account.

Librarians can:

- View books
- Search books
- Add books
- Remove books
- View borrowing records

### `Book`

`Book` represents a library book and manages information such as:

- Book ID
- Title
- Author
- Category
- Quantity
- Availability

The class provides methods for borrowing and returning books.

### `BorrowRecord`

`BorrowRecord` represents a borrowing transaction.

It stores information about:

- The borrowing user
- The borrowed book
- Borrowing status
- Return status
- Transaction information

---

# Encapsulation

The application uses properties to control access to important object attributes.

Validation is performed when values are assigned to protected attributes.

For example, user and book information is validated before being accepted by the model classes.

This helps maintain valid object state throughout the application.

---

# Inheritance and Polymorphic Behaviour

The system uses inheritance to avoid duplication between user types.

```text
User
├── Student
└── Librarian
```

Both `Student` and `Librarian` inherit common functionality from `User` while providing role-specific behaviour.

This allows the system to treat users consistently while still enforcing different permissions.

---

# Authentication and Authorization

The system separates authentication from authorization.

### Authentication

Authentication verifies that a user has valid login credentials.

The authentication service:

- Registers users.
- Checks usernames.
- Verifies passwords.
- Creates user objects.
- Assigns unique user IDs.
- Supports login and logout operations.

### Authorization

Authorization determines what an authenticated user is allowed to do.

The system supports two main roles:

- `student`
- `librarian`

Role-based restrictions prevent users from performing operations outside their permissions.

For example:

- Students cannot add or remove books.
- Librarians can manage the catalogue.
- Librarians can view borrowing records.
- Students can view their own borrowing records.

---

## Password Security

Passwords are securely hashed using **bcrypt** before being stored in the JSON user database. Plain-text passwords are not stored during normal registration.

The authentication system uses salted bcrypt hashes to protect user passwords. It also supports legacy SHA-256 and plain-text passwords from earlier versions of the application. When a user successfully logs in with a legacy password, the system automatically upgrades the stored password to a bcrypt hash.

A SHA-256 pre-hashing step is applied before bcrypt to safely support passwords longer than bcrypt's 72-byte input limit.

**Security features:**
- Salted bcrypt password hashing.
- Password verification during login.
- Support for legacy password formats.
- Automatic migration of legacy passwords to bcrypt.
- No plain-text password storage during normal registration.
---

# Command-Line Interface

The application provides both an interactive menu and command-line commands.

The CLI is implemented using Python's built-in `argparse` module.

## Start the Interactive Application

From the project root:

```bash
python3 main.py
```

The interactive interface allows the user to navigate the system through menus.

---

# CLI Commands

The application also supports individual command-line operations.

## Display Help

```bash
python3 main.py --help
```

This displays the available commands and their usage.

## Start Interactive Mode

```bash
python3 main.py interactive
```

## Register a User

```bash
python3 main.py register
```

Registration prompts the user for the required account information.

## Login

```bash
python3 main.py login --username USERNAME
```

Example:

```bash
python3 main.py login --username felix
```

The command prompts for the user's password.

## View Books

```bash
python3 main.py books --username USERNAME
```

Example:

```bash
python3 main.py books --username felix
```

## Search Books

```bash
python3 main.py search --term "Python" --username USERNAME
```

The search command supports searching the library catalogue.

## Borrow a Book

```bash
python3 main.py borrow --book-id BOOK_ID --username USERNAME
```

Example:

```bash
python3 main.py borrow --book-id B001 --username felix
```

## Return a Book

```bash
python3 main.py return --book-id BOOK_ID --username USERNAME
```

Example:

```bash
python3 main.py return --book-id B001 --username felix
```

## View Borrowing Records

```bash
python3 main.py records --username USERNAME
```

The command displays the borrowing records available to the authenticated user according to their role.

---

# Data Persistence

The application uses JSON files for persistent storage.

The main data files are:

### `data/users.json`

Stores registered user information, including:

- User ID
- Username
- Password information
- User role

### `data/books.json`

Stores:

- Book IDs
- Book titles
- Authors
- Categories
- Quantities
- Availability information

### `data/borrow_records.json`

Stores borrowing and return transactions.

Because data is stored in JSON files, information can persist after the application is closed and restarted.

---

# File Handling and Error Management

The project includes a reusable JSON management utility in:

```text
utils/json_manager.py
```

The JSON manager handles:

- Loading JSON data.
- Saving JSON data.
- Missing files.
- Invalid or malformed JSON.
- File access errors.
- JSON formatting.

This separates file handling from the business logic and makes the application easier to maintain and test.

---

# Decorators

The project uses reusable decorators to separate common functionality from business logic.

The decorators are located in:

```text
utils/decorators.py
```

## `@login_required`

Restricts protected operations to authenticated users.

## `@role_required()`

Restricts operations based on the user's role.

For example, librarian-only operations cannot be accessed by student accounts.

## `@log_action`

Records application activity in:

```text
logs/library.log
```

Using decorators reduces duplicated authorization and logging code across the application.

---

# Input Validation

Input validation is implemented in:

```text
utils/validators.py
```

The validation utilities help ensure that:

- Required values are not empty.
- Passwords meet the required minimum length.
- Menu choices are valid.
- Invalid input is handled without crashing the application.

---

# Application Services

Business logic is separated into service classes/modules.

## `services/auth_service.py`

Responsible for authentication-related operations, including:

- Registration
- Login
- Logout
- Password verification
- User lookup
- Role handling
- User persistence

## `services/library_service.py`

Responsible for library operations, including:

- Viewing books
- Searching books
- Adding books
- Removing books
- Borrowing books
- Returning books
- Viewing borrowing records

This separation keeps the application modular and reusable.

---

# Testing

The project uses `pytest` for automated testing.

Tests cover the major components of the application.

Test files include:

```text
tests/
├── test_auth_service.py
├── test_book.py
├── test_borrow_record.py
├── test_cli.py
├── test_json_manager.py
├── test_library_service.py
├── test_user.py
└── test_validators.py
```

The test suite covers:

- User functionality
- Student and librarian behaviour
- Authentication
- Registration
- Password verification
- Book operations
- Borrowing and returning
- Borrow records
- JSON file handling
- Validation
- Decorator-protected operations
- CLI behaviour

## Run the Tests

Install the dependencies first:

```bash
python3 -m pip install -r requirements.txt
```

Then run:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

---

# Logging and Debugging

Application activities are recorded in:

```text
logs/library.log
```

Logging provides a record of important operations and assists with debugging.

The project also uses automated tests to identify regressions and verify that major components continue to work correctly after changes.

---

# Installation and Setup

## Prerequisites

The project requires:

- Python 3
- pip
- Git (if cloning from GitHub)

Check the Python version:

```bash
python3 --version
```

Check pip:

```bash
python3 -m pip --version
```

---

## Clone the Repository

```bash
git clone https://github.com/felixouma10/Library_Management_System.git
```

Move into the project directory:

```bash
cd Library_Management_System
```

---

## Install Dependencies

Install the dependencies listed in `requirements.txt`:

```bash
python3 -m pip install -r requirements.txt
```

---

# Running the Project

Start the interactive application:

```bash
python3 main.py
```

Alternatively:

```bash
python3 main.py interactive
```

To see the available CLI commands:

```bash
python3 main.py --help
```

---

# Git and GitHub Workflow

The project is managed using Git and GitHub.

The development workflow includes:

- Feature branches
- Meaningful commits
- Pull requests
- Code review
- Merging completed features into the main branch

Example feature branch:

```bash
git switch -c feature/library-system-improvements
```

Check the current Git status:

```bash
git status
```

View commit history:

```bash
git log --oneline
```

Push a feature branch:

```bash
git push -u origin feature/library-system-improvements
```

---

# Code Quality and Reusability

The application is divided into separate modules according to responsibility.

```text
models/     → Application data and domain objects
services/   → Business logic
utils/      → Reusable utilities and decorators
data/       → Persistent JSON data
logs/       → Application logs
tests/      → Automated tests
main.py     → Command-line interface and application entry point
```

This structure makes the application easier to:

- Understand
- Test
- Maintain
- Extend
- Debug
- Reuse

---

# Error Handling

The application handles common errors including:

- Invalid user input
- Invalid menu selections
- Invalid login credentials
- Duplicate usernames
- Invalid book operations
- Attempting to borrow unavailable books
- Attempting to return books that were not borrowed
- Missing JSON files
- Malformed JSON data
- File read/write errors
- Unauthorized operations

Errors are handled with user-friendly messages rather than allowing expected application errors to terminate the program unexpectedly.

---

# Project Goals

The main goals of the project are to demonstrate practical Python programming concepts including:

1. Object-Oriented Programming
2. Inheritance
3. Encapsulation
4. Polymorphic behaviour
5. Authentication
6. Role-based authorization
7. File I/O
8. JSON persistence
9. Command-line application development
10. Decorators
11. Input validation
12. Exception handling
13. Logging
14. Automated testing
15. Modular code organization
16. Git and GitHub workflow

---

# Conclusion

The Library Management System demonstrates how Python can be used to build a modular command-line application using Object-Oriented Programming and software engineering practices.

The project combines:

- OOP design
- Modular architecture
- Authentication and authorization
- JSON persistence
- CLI commands
- Validation
- Error handling
- Decorators
- Logging
- Automated testing
- Git/GitHub version control

The structure is designed to make the system maintainable and provide a foundation for adding additional library functionality in the future.