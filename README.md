# Library Management System

A Python command-line Library Management System built using Object-Oriented Programming (OOP).

The system allows students to browse, search, borrow, and return books, while librarians can manage the catalogue and monitor borrowing records.

The project demonstrates classes, inheritance, encapsulation, decorators, JSON persistence, authentication, role-based authorization, input validation, exception handling, logging, and automated testing.

## Features

### Student Features
- Register a student account.
- Log in and log out.
- View the library catalogue.
- Search books by title, author, or category.
- Borrow available books.
- Return borrowed books.
- View personal borrowing records.

### Librarian Features
- Log in and log out.
- View and search the library catalogue.
- Add new books.
- Remove available books.
- View borrowing records.

### System Features
- Role-based access control.
- Password hashing.
- JSON-based data persistence.
- Input validation and error handling.
- Activity logging using decorators.
- Modular application structure.
- Automated tests using pytest.

## Technologies

| Technology | Purpose |
|---|---|
| Python 3 | Application development |
| JSON | Persistent storage |
| pytest | Automated testing |
| Git and GitHub | Version control and collaboration |
| argparse | Command-line argument parsing |

## Project Structure

```text
Library_Management_System/
├── main.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── student.py
│   ├── librarian.py
│   ├── book.py
│   └── borrow_record.py
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   └── library_service.py
├── utils/
│   ├── __init__.py
│   ├── decorators.py
│   ├── validators.py
│   └── json_manager.py
├── data/
│   ├── users.json
│   ├── books.json
│   └── borrow_records.json
├── logs/
│   └── library.log
├── tests/
│   ├── test_auth_service.py
│   ├── test_book.py
│   ├── test_borrow_record.py
│   ├── test_cli.py
│   ├── test_json_manager.py
│   ├── test_library_service.py
│   ├── test_user.py
│   └── test_validators.py
├── requirements.txt
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── README.md
```

## Object-Oriented Design

The application uses inheritance, encapsulation, and reusable classes.

- **User:** Base class containing shared user information and functionality.
- **Student:** Inherits from `User` and represents a student.
- **Librarian:** Inherits from `User` and represents a librarian.
- **Book:** Represents a book and manages its availability.
- **BorrowRecord:** Tracks borrowing and return transactions.

## Authentication and Authorization

Authentication verifies a user's credentials, while authorization determines which operations that user may perform.

The system distinguishes between student and librarian roles and restricts protected operations accordingly.

Passwords are hashed before being stored. The current SHA-256 implementation is intended for this educational project and should be replaced with a dedicated password-hashing algorithm for production use.

## Decorators

The application uses three reusable decorators:

- `@login_required` — restricts access to authenticated users.
- `@role_required()` — restricts operations according to user role.
- `@log_action` — records application activities in `logs/library.log`.

## Data Persistence

The application uses JSON files for storage:

- `data/users.json` — registered users and their roles.
- `data/books.json` — book details and availability.
- `data/borrow_records.json` — borrowing and return transactions.

Data is saved to JSON files so it can persist between application sessions.

## Installation and Setup

### Prerequisites

- Python 3 installed.
- Git installed if cloning the repository.

Check your Python installation:

```bash
python3 --version
```

### Clone the Repository

```bash
git clone https://github.com/felixouma10/Library_Management_System.git
cd Library_Management_System
```

### Install Dependencies

Install the project's Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Running the Application

Start the interactive application:

```bash
python