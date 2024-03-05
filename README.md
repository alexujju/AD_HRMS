Please ensure to create config.py file with mongo_URI.


We also need to add config.ini in backend/ad_auth
___________________________________________________________________________
Format of config.ini

[LDAP]
SERVER = ldap://xx.xx.xx.xx
PORT = 389
BASE_DN = cn= Users dc=testad,dc=local
DOMAIN = domain name (example) testad.local
USERNAME = administrator
PASSWORD = password

____________________________________________________________________________