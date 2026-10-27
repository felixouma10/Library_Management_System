def validate_not_empty(value, field_name):
    """Validate that a value is not empty."""

    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")

    return value.strip()


def validate_password(password):
    """Validate that a password meets the minimum length."""

    if len(password) < 4:
        raise ValueError(
            "Password must be at least 4 characters long."
        )

    return password


def get_menu_choice(minimum, maximum):
    """Get and validate a numeric menu choice."""

    while True:
        try:
            choice = int(input("Enter your choice: "))

            if minimum <= choice <= maximum:
                return choice

            print(
                f"Please enter a number between "
                f"{minimum} and {maximum}."
            )

        except ValueError:
            print("Invalid input. Please enter a number.")