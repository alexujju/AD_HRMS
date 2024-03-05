from flask import Blueprint, request, jsonify
import os
from backend.Models.user_dao import UserDao
from backend.Models.users_models import User
from ..ad_auth.ad_authenticate import ActiveDirectory
import logging

users_bp = Blueprint('users', __name__)
user_dao = UserDao()
active_directory = ActiveDirectory()  # Create an instance of ActiveDirectory

# Path to the log file
log_file = "user_creation_log.txt"

# Configure logging
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Onboarding form route
@users_bp.route('/onboard', methods=['POST'])
def onboard_user():
    AD_conn = None
    try:
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

        # Validate username
        existing_user = user_dao.find_user_by_username(username)
        if existing_user:
            return jsonify({'error': 'User with the same username already exists'}), 400

        # Check if user with the same email address exists
        existing_email = user_dao.find_user_by_email(email)
        if existing_email:
            return jsonify({'error': 'User with the same email address already exists'}), 400

        new_user = User(username, email, department, emp_id, display_name, first_name, last_name,
                        line_manager, laptop_status, phone_number, designation)
        inserted_id = user_dao.insert_user(new_user)

        # Establish connection with Active Directory using LDAP configuration
        AD_conn, server_uri = active_directory.connect()
        if not AD_conn:
            logging.error("Failed to connect to Active Directory")
            return jsonify({'error': 'Failed to connect to Active Directory'}), 500

        # Create user in Active Directory
        success = active_directory.create_user(AD_conn, username, email, department, emp_id, display_name, first_name, last_name, phone_number, designation)

        if success:
            logging.info("User onboarded successfully and created in Active Directory")
            return jsonify({'message': 'User onboarded successfully and created in Active Directory'}), 200
        else:
            logging.error("Failed to create user in Active Directory")
            return jsonify({'error': 'Failed to create user in Active Directory. See log for details.'}), 500

    except Exception as e:
        logging.error(f"Error during user onboarding: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if AD_conn:
            AD_conn.unbind()
        
