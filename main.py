from storage import StorageManager
from book import BookManager
from user import UserManager
from check import CheckoutManager
import datetime
import logging
import os

# Setting up logging
logging.basicConfig(filename='library_management.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class LibraryManagementSystem:
    def __init__(self):
        # Initializing managers
        self.storage_manager = StorageManager()
        self.book_manager = BookManager()
        self.user_manager = UserManager()
        self.checkout_manager = CheckoutManager(self.user_manager, self.book_manager)
        self.load_data()
        logging.info("Library Management System initialized")

    def load_data(self):
        # Loading data from storage
        data = self.storage_manager.load_data()
        if not isinstance(data, dict):
            data = {}
        # Populating managers with loaded data
        self.book_manager.books = data.get('books', [])
        self.user_manager.users = data.get('users', [])
        self.checkout_manager.checkouts = data.get('checkouts', [])

    def save_data(self):
        # Saving data to storage
        data = {
            'books': [book.__dict__ for book in self.book_manager.books],
            'users': [user.__dict__ for user in self.user_manager.users],
            'checkouts': [checkout.__dict__ for checkout in self.checkout_manager.checkouts]
        }
        self.storage_manager.save_data(data)

    def clear_screen(self):
        # Clearing the console screen
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title):
        # Printing formatted header
        self.clear_screen()
        print(f"{'-' * 10} {title} {'-' * 10}\n")

    def run(self):
        # Main program loop
        while True:
            self.print_header("Library Management System")
            print("1. Manage Books")
            print("2. Manage Users")
            print("3. Manage Checkouts")
            print("4. Exit")
            choice = input("\nEnter choice: ")

            if choice == '1':
                self.manage_books()
            elif choice == '2':
                self.manage_users()
            elif choice == '3':
                self.manage_checkouts()
            elif choice == '4':
                self.save_data()
                break
            else:
                print("\nInvalid option, please try again.")

    def manage_books(self):
        # Book management submenu
        while True:
            print("\n1. Add Book")
            print("2. Update Book")
            print("3. Delete Book")
            print("4. List Books")
            print("5. Search Books")
            print("6. Go Back")
            choice = input("Enter choice: ")

            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.update_book()
            elif choice == '3':
                self.delete_book()
            elif choice == '4':
                self.list_books()
            elif choice == '5':
                self.search_books()
            elif choice == '6':
                break
            else:
                print("Invalid option, please try again.")

    def add_book(self):
        # Adding a new book
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        isbn = input("Enter book ISBN: ")
        self.book_manager.add_book(title, author, isbn)
        print("Book added successfully.")
        logging.info(f"Book added: {title}, {author}, {isbn}")

    def update_book(self):
        # Updating an existing book
        isbn = input("Enter book ISBN to update: ")
        title = input("Enter new title (press enter to skip): ")
        author = input("Enter new author (press enter to skip): ")
        if self.book_manager.update_book(isbn, title if title else None, author if author else None):
            print("Book updated successfully.")
            logging.info(f"Book updated: {isbn}, New title: {title}, New author: {author}")
        else:
            print("Book update failed. No such book available")
            logging.warning(f"Book update failed for ISBN: {isbn}")

    def delete_book(self):
        # Deleting a book
        isbn = input("Enter book ISBN to delete: ")
        if self.book_manager.delete_book(isbn):
            print("Book deleted successfully.")
            logging.info(f"Book deleted: ISBN {isbn}")
        else:
            print("Book deletion failed.")
            logging.warning(f"Book deletion failed for ISBN: {isbn}")

    def list_books(self):
        # Listing all books
        books = self.book_manager.list_books()
        for book in books:
            is_checked_out = any(checkout.book.isbn == book.isbn for checkout in self.checkout_manager.checkouts)
            status = "Checked Out" if is_checked_out else "Available"
            print(f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}, Status: {status}")

    def search_books(self):
        # Searching for books
        print("\n1. Search by Title")
        print("2. Search by Author")
        print("3. Search by ISBN")
        choice = input("Enter choice: ")
        if choice == '1':
            title = input("Enter title to search: ")
            books = self.book_manager.search_books(title=title)
        elif choice == '2':
            author = input("Enter author to search: ")
            books = self.book_manager.search_books(author=author)
        elif choice == '3':
            isbn = input("Enter ISBN to search: ")
            books = self.book_manager.search_books(isbn=isbn)
        else:
            print("Invalid option")
            return

        if books:
            for book in books:
                print(f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}")
        else:
            print("No books found.")

    def manage_checkouts(self):
        # Checkout management submenu
        while True:
            print("\n1. Checkout Book")
            print("2. Return Book")
            print("3. List All Checkouts")
            print("4. Go Back")
            choice = input("Enter choice: ")

            if choice == '1':
                self.checkout_book()
            elif choice == '2':
                self.return_book()
            elif choice == '3':
                self.list_checkouts()
            elif choice == '4':
                break
            else:
                print("Invalid option, please try again.")

    def checkout_book(self):
        # Checking out a book
        user_id = input("Enter user ID: ")
        isbn = input("Enter book ISBN: ")
        book = self.book_manager.find_book_by_isbn(isbn)
        if not book:
            print("Book not found.")
            return
        if any(checkout.book_isbn == isbn for checkout in self.checkout_manager.checkouts):
            print("Book is already checked out.")
            return
        checkout_date = datetime.date.today()
        result = self.checkout_manager.checkout_book(user_id, isbn, checkout_date)
        if result:
            print("Book checked out successfully.")
            logging.info(f"Book checked out: ISBN {isbn}, User ID {user_id}")
        else:
            print("Checkout failed.")

    def return_book(self):
        # Returning a book
        user_id = input("Enter user ID: ")
        isbn = input("Enter book ISBN: ")
        return_date = datetime.date.today()
        result = self.checkout_manager.return_book(user_id, isbn, return_date)
        if result:
            print("Book returned successfully.")
            logging.info(f"Book returned: ISBN {isbn}, User ID {user_id}")
        else:
            print("Return failed.")

    def list_checkouts(self):
        # Listing all checkouts
        checkouts = self.checkout_manager.list_checkouts()
        if checkouts:
            for checkout in checkouts:
                print(f"User ID: {checkout.user_id}, Book ISBN: {checkout.book_isbn}, Checkout Date: {checkout.checkout_date}")
        else:
            print("No checkouts available.")

    def manage_users(self):
        # User management submenu
        while True:
            print("\n1. Add User")
            print("2. Update User")
            print("3. Delete User")
            print("4. List Users")
            print("5. Search Users")
            print("6. Go Back")
            choice = input("Enter choice: ")

            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.update_user()
            elif choice == '3':
                self.delete_user()
            elif choice == '4':
                self.list_users()
            elif choice == '5':
                self.search_users()
            elif choice == '6':
                break
            else:
                print("Invalid option, please try again.")

    def add_user(self):
        # Adding a new user
        name = input("Enter user name: ")
        user_id = input("Enter user ID: ")
        if self.user_manager.add_user(name, user_id):
            print("User added successfully.")
            logging.info(f"User added: {name}, ID {user_id}")
        else:
            print("User already exists.")
            logging.warning(f"User addition failed: {name}, ID {user_id}")

    def update_user(self):
        # Updating an existing user
        user_id = input("Enter user ID to update: ")
        new_name = input("Enter new name: ")
        if self.user_manager.update_user(user_id, new_name):
            print("User updated successfully.")
            logging.info(f"User updated: ID {user_id}, New name: {new_name}")
        else:
            print("User update failed or no changes made.")
            logging.warning(f"User update failed for ID: {user_id}")

    def delete_user(self):
        # Deleting a user
        user_id = input("Enter user ID to delete: ")
        if self.user_manager.delete_user(user_id):
            print("User deleted successfully.")
            logging.info(f"User deleted: ID {user_id}")
        else:
            print("User not found.")
            logging.warning(f"User deletion failed for ID: {user_id}")

    def list_users(self):
        # Listing all users
        users = self.user_manager.list_users()
        if users:
            for user in users:
                print(f"Name: {user.name}, User ID: {user.user_id}")
        else:
            print("No users available.")

    def search_users(self):
        # Searching for users
        print("\n1. Search by Name")
        print("2. Search by User ID")
        choice = input("Enter choice: ")
        if choice == '1':
            name = input("Enter name to search: ")
            users = self.user_manager.search_users(name=name)
        elif choice == '2':
            user_id = input("Enter user ID to search: ")
            users = self.user_manager.search_users(user_id=user_id)
        else:
            print("Invalid option")
            return

        if users:
            for user in users:
                print(f"Name: {user.name}, User ID: {user.user_id}")
        else:
            print("No users found.")

def main():
    # Initializing and running the library management system
    system = LibraryManagementSystem()
    system.run()

if __name__ == "__main__":
    main()
