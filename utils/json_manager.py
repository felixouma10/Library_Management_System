import json
import os


class JSONManager:
    """Handle loading and saving JSON data."""

    @staticmethod
    def load(filename):
        """Load data from a JSON file."""

        try:

            if not os.path.exists(filename):
                return []

            with open(
                filename,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except json.JSONDecodeError:

            print(
                f"Error: {filename} "
                f"contains invalid JSON."
            )

            return []

        except OSError as error:

            print(
                f"Error reading {filename}: "
                f"{error}"
            )

            return []

    @staticmethod
    def save(filename, data):
        """Save data to a JSON file."""

        try:

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

        except OSError as error:

            print(
                f"Error saving data: "
                f"{error}"
            )