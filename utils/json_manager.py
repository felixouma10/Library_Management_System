import json
import os


class JSONManager:

    @staticmethod
    def load(filename):
        try:
            if not os.path.exists(filename):
                return []

            with open(filename, "r") as file:
                return json.load(file)

        except json.JSONDecodeError:
            print(f"Error: {filename} contains invalid JSON.")
            return []

        except OSError as error:
            print(f"Error reading {filename}: {error}")
            return []

    @staticmethod
    def save(filename, data):
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)

        except OSError as error:
            print(f"Error saving data: {error}")