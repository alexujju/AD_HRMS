from flask import Flask, jsonify
from connection import client
from config import Config
from backend.routes import users_bp
from bson import ObjectId 

app = Flask(__name__)
app.config.from_object(Config)

# Check if PyMongo is properly initialized
print("PyMongo initialized:", client.db is not None)

@app.route('/users')
def get_users():
    try:
        # Access the users collection from MongoDB
        if client.db is None:
            raise Exception("MongoDB connection is not initialized.")
        # Specify the database name and collection name explicitly
        print("Database:", client.get_database())
        db = client.get_database('Tests_accounts')
        print("Database connected successfully")
        users_collection = db.get_collection('users')
        
        # Query documents from the collection
        users = list(users_collection.find())

        # Serialize ObjectId fields to strings
        for user in users:
            user['_id'] = str(user['_id'])

        return jsonify(users)
    except Exception as e:
        return f"An error Occurred: {str(e)}"

# Register blueprint for user routes
app.register_blueprint(users_bp, url_prefix='/users')

if __name__ == '__main__':
    app.run(debug=True)
