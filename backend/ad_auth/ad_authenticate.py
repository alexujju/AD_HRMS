import os
import logging
import configparser
from ldap3 import Server, Connection, ALL

log_file_path = os.path.join(os.getcwd(), "ad_auth.log")


class ActiveDirectory:
    def __init__(self):
        self.config = self.load_config()
        self.server_uri = self.config['LDAP']['SERVER']
        self.base_dn = self.config['LDAP']['BASE_DN']
        self.domain = self.config['LDAP']['DOMAIN']
        self.bind_dn = self.config['LDAP']['USERNAME']
        self.bind_password = self.config['LDAP']['PASSWORD']
        
        # Configure logging
        logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_config(self):
        current_dir = os.path.dirname(__file__)
        config_file = os.path.join(current_dir, 'config.ini')
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def connect(self):
        try:
            server = Server(self.server_uri, get_info=ALL)
            conn = Connection(server, user=f"{self.bind_dn}@{self.domain}", password=self.bind_password, auto_bind=True)
            logging.info(f"Successfully connected to Active Directory: {self.server_uri}")
            return conn, self.server_uri
        except Exception as e:
            logging.error(f"Failed to connect to Active Directory: {e}")
            return None, None

    def create_user(self, AD_conn, username, email, department, emp_id, display_name, first_name, last_name, phone_number, designation):
        logging.debug(f"Arguments received: conn={AD_conn}, username={username}, email={email}, department={department}, emp_id={emp_id}, display_name={display_name}, first_name={first_name}, last_name={last_name}, phone_number={phone_number}, designation={designation}")
        try:
            if not AD_conn:
                logging.error("Connection object is not initialized.")
                return False
            
            if not AD_conn.bind():
                logging.error("Failed to bind to Active Directory.")
                return False

            base_dn = 'CN=Users,DC=testad,DC=local'
            user_attributes = {
                'cn': display_name,
                'givenName': first_name,
                'sn': last_name,
                'userPrincipalName': email,
                'department': department,
                'employeeID': emp_id,
                'telephoneNumber': phone_number,
                'title': designation,
                'sAMAccountName': username,  # Corrected attribute name
                'userPassword': 'password123',
                'objectClass': ['top', 'person', 'organizationalPerson', 'user']
            }

            AD_conn.add(f"cn={user_attributes['cn']},{base_dn}", attributes=user_attributes)

            if AD_conn.result['result'] == 0:
                logging.info(f"User '{username}' created successfully in Active Directory.")
                return True
            else:
                error_description = AD_conn.result['description']
                logging.error(f"Failed to create user. LDAP error: {error_description}")
                return False
        except Exception as e:
            logging.error(f"Failed to create user '{username}' in Active Directory: {e}")
            return False
        finally:
            AD_conn.unbind()
