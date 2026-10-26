# Library Management System

A **Python CLI Library Management System** built using Object-Oriented Programming (OOP).

The system allows **students** to browse, search, borrow and return books, while **librarians** can manage books and monitor borrowing records.

The project demonstrates practical use of **Python classes, inheritance, encapsulation, decorators, JSON persistence, authentication, authorization, validation, error handling, and logging**.

---

## Features

Students can:

-  Login securely
-  View the library catalogue
-  Search books by title, author, or category
-  Borrow available books
-  Return borrowed books
-  View personal borrowing records
-  Logout

Librarians can:

- Login securely
- View all books
- Search the library catalogue
- Add new books
- Remove available books
- View all borrowing records
- Logout

### System Features

- Role-based access control
- Authentication and authorization
- JSON-based data persistence
- Input validation
- Error handling
- Activity logging
- Modular project structure
- Object-oriented design
- Reusable decorators
- Interactive command-line interface

---

## Technologies

| Technology | Purpose |
|---|---|
| **Python 3** | Programming language |
| **JSON** | Data |
| **OOP** | Application blueprint |
| **Decorators** | Authentication, authorization & logging |
| **CLI** | User interface |
| **Git/GitHub** | Version control |

No external Python packages are required.

---

## Project Structure

```text
Library-Management/
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
└── README.md
```

---

## Object-Oriented Design

The project uses inheritance to represent different types of users.

### `User`

The base class containing common user information and functionality.

### `Student`

Inherits from `User` and represents a student using the library.

### `Librarian`

Inherits from `User` and represents a librarian responsible for managing the library.

### `Book`

Represents a library book and manages its availability.

### `BorrowRecord`

Records borrowing transactions between students and books.

---

## Authentication & Authorization

The system separates **authentication** from **authorization**.

### Authentication

Determines whether the user's credentials are valid.

```text
Username + Password
        ↓
   AuthService
        ↓
Authenticated User
```

### Authorization

Determines what the authenticated user is allowed to do.

For example:

```python
@role_required("librarian")
def add_book(...):
    ...
```

Only librarians can access librarian-specific operations.

---

## Decorators

The project includes three reusable decorators.

### `@login_required`

Prevents users from accessing protected functionality without logging in.

### `@role_required()`

Restricts functionality according to the user's role.

### `@log_action`

Records user actions in:

```text
logs/library.log
```

Example:

```text
2026-10-26 14:20:15 - john - borrow_book
```

---

## Data

The application uses JSON files instead of a database.

### Users

```text
data/users.json
```

Stores registered students and librarians.

### Books

```text
data/books.json
```

Stores the library catalogue and book availability.

### Borrowing Records

```text
data/borrow_records.json
```

Stores borrowing and return transactions.

This allows the application's data to persist even after the program is closed.

---

## Getting Started

### Requirements

Make sure Python 3 is installed.

Check your Python version:

```bash
python --version
```

or:

```bash
python3 --version
```

### Clone the repository

```bash
git clone https://github.com/felixouma10/Library_Management_System
```

Navigate into the project:

```bash
cd Library-Management
```

### Run the application

```bash
python3 main.py
```

---

##  Demo Accounts

The project includes sample accounts in `data/users.json`.

### Student

```text
Username: felix
Password: 1234
```

### Librarian

```text
Username: faith
Password: admin123
```
---

## Application Flow

### Login

```text
      LIBRARY MANAGEMENT SYSTEM 
1. Login
2. Exit
```

After successful authentication, the appropriate menu is displayed based on the user's role.

### Student Menu

```text
      STUDENT MENU 
1. View all books
2. Search books
3. Borrow a book
4. Return a book
5. View my borrowing records
6. Logout
```

### Librarian Menu

```text
      LIBRARIAN MENU 
1. View all books
2. Search books
3. Add a book
4. Remove a book
5. View all borrowing records
6. Logout
```

---

##  Borrowing Workflow

When a student borrows a book:

```text
Student selects book
        ↓
System checks book exists
        ↓
System checks availability
        ↓
Book marked as unavailable
        ↓
BorrowRecord created
        ↓
Data saved to JSON
```

When the book is returned:

```text
Student selects book
        ↓
System finds active borrowing record
        ↓
Book marked as available
        ↓
BorrowRecord updated
        ↓
Return date recorded
        ↓
Data saved to JSON
```

---

## Error Handling

The system handles common invalid operations, including:

- Invalid username or password
- Empty input
- Invalid menu choices
- Book not found
- Borrowing an unavailable book
- Returning a book that was not borrowed
- Removing a borrowed book
- Invalid JSON data
- File access errors

The application displays an appropriate error message instead of terminating unexpectedly.

---

## Learning Objectives

This project was developed to demonstrate practical understanding of:

- Python programming
- Object-Oriented Programming
- Classes and objects
- Encapsulation
- Inheritance
- Polymorphism
- Modular programming
- Decorators
- File handling
- JSON serialization
- Authentication
- Role-based authorization
- Input validation
- Exception handling
- Logging
- CLI application development

---

## Contributing

Contributions, suggestions, and improvements are welcome.

To contribute:

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/your-feature
```

3. Make your changes
4. Commit your changes

```bash
git commit -m "Add your feature"
```

5. Push to your branch

```bash
git push origin feature/your-feature
```

6. Open a Pull Request

---

## License

This project is available for educational and learning purposes.

---

## Author

**Felix Ouma**

Built with Python