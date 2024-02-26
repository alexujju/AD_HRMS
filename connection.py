from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import Config

# Initialize MongoDB client
client = MongoClient(Config.MONGO_URI, server_api=ServerApi('1'))