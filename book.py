class Book:
    def __init__(self, title, author, isbn):
        # Initialize a Book object with title, author, and ISBN
        self.title = title
        self.author = author
        self.isbn = isbn

    def __str__(self):
        # Return a formatted string representation of the Book object
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}"

class BookManager:
    def __init__(self):
        # Initialize a BookManager object with an empty list of books
        self.books = []

    def add_book(self, title, author, isbn):
        # Add a new book to the book list
        new_book = Book(title, author, isbn)
        self.books.append(new_book)

    def update_book(self, isbn, title=None, author=None):
        # Update an existing book's title and/or author
        book = self.find_book_by_isbn(isbn)
        if book:
            if title:
                book.title = title
            if author:
                book.author = author
            return True
        return False

    def delete_book(self, isbn):
        # Delete a book from the book list by ISBN
        for i, book in enumerate(self.books):
            if book.isbn == isbn:
                del self.books[i]
                return True
        return False

    def list_books(self):
        # Return a list of all books
        return self.books if self.books else []

    def find_book_by_isbn(self, isbn):
        # Find and return a book by its ISBN
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def search_books(self, title=None, author=None):
        # Search for books by title and/or author
        results = []
        for book in self.books:
            if title and title in book.title:
                results.append(book)
            elif author and author in book.author:
                results.append(book)
        return results
