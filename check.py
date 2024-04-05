from models import Checkout

class CheckoutManager:
    def __init__(self, user_manager, book_manager):
        # Initialize a CheckoutManager object with user_manager, book_manager, and an empty list of checkouts
        self.user_manager = user_manager
        self.book_manager = book_manager
        self.checkouts = []

    def checkout_book(self, user_id, isbn, checkout_date):
        # Checkout a book for a user
        user = self.user_manager.find_user_by_id(user_id)
        book = self.book_manager.find_book_by_isbn(isbn)

        if user and book:
            # Create a Checkout object and add it to the checkouts list
            checkout = Checkout(user, book, checkout_date)
            self.checkouts.append(checkout)
            return True
        return False

    def return_book(self, user, book, return_date):
        # Mark a book as returned by updating the return_date in the corresponding Checkout object
        for checkout in self.checkouts:
            if checkout.user == user and checkout.book == book:
                checkout.return_date = return_date
                break

    def list_checkouts(self):
        # List all checkouts
        for checkout in self.checkouts:
            print(checkout)
