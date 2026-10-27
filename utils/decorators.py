from functools import wraps
from datetime import datetime


def login_required(function):
    """Require the user to be logged in."""

    @wraps(function)
    def wrapper(self, *args, **kwargs):

        if self.current_user is None:

            print(
                "\nPlease login first."
            )

            return None

        return function(
            self,
            *args,
            **kwargs
        )

    return wrapper


def role_required(required_role):
    """Restrict a function to a specific user role."""

    def decorator(function):

        @wraps(function)
        def wrapper(self, *args, **kwargs):

            if self.current_user is None:

                print(
                    "\nPlease login first."
                )

                return None

            if self.current_user.role != required_role:

                print(
                    f"\nAccess denied. "
                    f"{required_role.title()} "
                    f"privileges required."
                )

                return None

            return function(
                self,
                *args,
                **kwargs
            )

        return wrapper

    return decorator


def log_action(function):
    """Log successful system actions."""

    @wraps(function)
    def wrapper(self, *args, **kwargs):

        result = function(
            self,
            *args,
            **kwargs
        )

        try:

            with open(
                "logs/library.log",
                "a",
                encoding="utf-8"
            ) as file:

                username = (
                    self.current_user.username
                    if self.current_user
                    else "Unknown"
                )

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                file.write(
                    f"{timestamp} - "
                    f"{username} - "
                    f"{function.__name__}\n"
                )

        except OSError:
            pass

        return result

    return wrapper