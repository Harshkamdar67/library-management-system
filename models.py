class Book:
    def __init__(self, title, author, isbn):
        # Initialize a Book object with title, author, and ISBN
        self.title = title
        self.author = author
        self.isbn = isbn

    def __str__(self):
        # Return a formatted string representation of the Book object
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}"

class User:
    def __init__(self, name, user_id):
        # Initialize a User object with name and user ID
        self.name = name
        self.user_id = user_id

    def __str__(self):
        # Return a formatted string representation of the User object
        return f"Name: {self.name}, User ID: {self.user_id}"

class Checkout:
    def __init__(self, user, book, checkout_date, return_date=None):
        # Initialize a Checkout object with user, book, checkout date, and optional return date
        self.user = user
        self.book = book
        self.checkout_date = checkout_date
        self.return_date = return_date

    def __str__(self):
        # Return a formatted string representation of the Checkout object
        return (f"Checkout - User: {self.user.name}, Book: {self.book.title}, "
                f"Checkout Date: {self.checkout_date}, Return Date: {self.return_date}")
