from datetime import datetime
from marshmallow import Schema, fields, validate


class User:
    def __init__(self, username, email, department, emp_id, display_name, first_name, last_name, line_manager, laptop_status, phone_number, designation, _id=None):
        self._id = _id  # You can keep this if you're using ObjectId
        self.username = username
        self.email = email
        self.department = department
        self.emp_id = emp_id
        self.display_name = display_name
        self.first_name = first_name
        self.last_name = last_name
        self.line_manager = line_manager
        self.laptop_status = laptop_status
        self.phone_number = phone_number
        self.designation = designation
        self.timestamp = datetime.utcnow()
    
    # If you're using ObjectId, you may want to serialize it to a string
    def serialize(self):
        return {
            '_id': str(self._id),
            'username': self.username,
            'email': self.email,
            'department': self.department,
            'emp_id': self.emp_id,
            'display_name': self.display_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'line_manager': self.line_manager,
            'laptop_status': self.laptop_status,
            'phone_number': self.phone_number,
            'designation': self.designation,
            'timestamp': self.timestamp
        }
    