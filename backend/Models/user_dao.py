from pymongo import MongoClient
from config import Config
from connection import client
from backend.Models.users_models import User
from datetime import datetime

class UserDao:
    def __init__(self):
        self.db = client.get_database('Tests_accounts')
        self.users_collection = self.db.get_collection('users')

    def insert_user(self, user):
        user_data = {
            'username': user.username,
            'email': user.email,
            'department': user.department,
            'emp_id': user.emp_id,
            'display_name': user.display_name,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'line_manager': user.line_manager,
            'laptop_status': user.laptop_status,
            'phone_number': user.phone_number,
            'designation': user.designation,
            'timestamp': datetime.utcnow()
  
        }
        result = self.users_collection.insert_one(user_data,)
        return result.inserted_id
    
    def count_users(self):
        try:
        # Count the total number of documents in the collection
            count = self.db.collection.estimated_document_count({})
            return count
        except Exception as e:
        # Log the error
            print(f"An error occurred while counting users: {e}")
        # Optionally, raise or return the error to handle it at a higher level
        raise e
    def find_user_by_username(self, username):
        # Query the database to find a user by username
        user = self.users_collection.find_one({'username': username})
        return user
    
    def find_user_by_email(self, email):
        # Query the database to find a user by username
        user = self.users_collection.find_one({'email': email})
        return user