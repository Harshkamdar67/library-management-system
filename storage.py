import json
from models import Book, User, Checkout

class StorageManager:
    def __init__(self, file_name='library_data.json'):
        # Initialize the StorageManager with a default file name for storing data
        self.file_name = file_name

    def save_data(self, data):
        # Save data to a JSON file
        with open(self.file_name, 'w') as file:
            json.dump(data, file, default=self._to_json, indent=4)

    def load_data(self):
        try:
            # Load data from the JSON file
            with open(self.file_name, 'r') as file:
                return json.load(file, object_hook=self._from_json)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return an empty list if the file is not found or decoding fails
            return []

    def _to_json(self, obj):
        # Convert custom objects (Book, User, Checkout) to JSON serializable format
        if isinstance(obj, (Book, User, Checkout)):
            return obj.__dict__
        # Raise an error if the object type is not supported
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    def _from_json(self, json_data):
        # Convert JSON data back to corresponding objects
        if 'isbn' in json_data:
            return Book(**json_data)  # Create a Book object
        elif 'user_id' in json_data:
            return User(**json_data)  # Create a User object
        elif 'checkout_date' in json_data:
            return Checkout(**json_data)  # Create a Checkout object
        # Return the JSON data if no matching object is found
        return json_data
