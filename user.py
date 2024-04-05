class User:
    def __init__(self, name, user_id):
        # Initialize a User object with name and user ID
        self.name = name
        self.user_id = user_id

    def __str__(self):
        # Return a formatted string representation of the User object
        return f"Name: {self.name}, User ID: {self.user_id}"

class UserManager:
    def __init__(self):
        # Initialize a UserManager object with an empty list of users
        self.users = []

    def add_user(self, name, user_id):
        # Add a new user to the user list if the user ID is not already in use
        if not any(user.user_id == user_id for user in self.users):
            user = User(name, user_id)
            self.users.append(user)
            return True
        return False

    def update_user(self, user_id, new_name=None):
        # Update an existing user's name
        user = self.find_user_by_id(user_id)
        if user and new_name:
            user.name = new_name
            return True
        return False

    def delete_user(self, user_id):
        # Delete a user from the user list by user ID
        for i, user in enumerate(self.users):
            if user.user_id == user_id:
                del self.users[i]
                return True
        return False

    def list_users(self):
        # Return a list of all users
        return self.users if self.users else []

    def find_user_by_id(self, user_id):
        # Find and return a user by user ID
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def search_users(self, name=None, user_id=None):
        # Search for users by name or user ID
        if name:
            return [user for user in self.users if user.name.lower() == name.lower()]
        elif user_id:
            return [user for user in self.users if user.user_id == user_id]
        return []
