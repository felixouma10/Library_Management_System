def validate_not_empty(value, field_name):
    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")

    return value.strip()


def get_menu_choice(minimum, maximum):
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