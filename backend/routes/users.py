from flask import Blueprint, request, jsonify
from connection import client
#from app import client
from datetime import datetime
from backend.Models.user_dao import UserDao
from backend.Models.users_models import User
from bson.json_util import dumps
from datetime import datetime

users_bp = Blueprint('users', __name__)
user_dao = UserDao()

# Onboarding form route
@users_bp.route('/onboard', methods=['GET', 'POST'])
def onboard_user():
    try:
        if request.method == 'GET':
            # Query MongoDB to get the count of onboarded users
            count = user_dao.count_users()
            # Convert the count to a string for serialization
            user_count = str(count)
            # Serialize the response using dumps() function
            response_data = dumps({'user_count': user_count})
            return response_data, 200, {'Content-Type': 'application/json'}
        
        
        elif request.method == 'POST':
            # Extract user data from the request JSON
            data = request.json
            username = data.get('username')
            email = data.get('email')
            department = data.get('department')
            emp_id = data.get('emp_id')
            display_name = data.get('display_name')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            line_manager = data.get('line_manager')
            laptop_status = data.get('laptop_status')
            phone_number = data.get('phone_number')
            designation = data.get('designation')
            

            #valdiation for username
            existing_user = user_dao.find_user_by_username(username)
            if existing_user:
                return jsonify({'error': 'User with the same username already exists'}), 400

            # Check if user with the same email address exists
            existing_email = user_dao.find_user_by_email(email)
            if existing_email:
                return jsonify({'error': 'User with the same email address already exists'}), 400


            new_user = User(username, email, department,emp_id, display_name, first_name, last_name, line_manager, laptop_status, phone_number, designation,)
            inserted_id = user_dao.insert_user(new_user)
            
            return jsonify({'message': 'User onboarded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500