def salutation(name):
    return f"Hello, {name}!"

message = salutation("felix")
print(message)


def add_book():
    title = input("Enter book title:")
    print(f"Book '{title}' added successfully!")