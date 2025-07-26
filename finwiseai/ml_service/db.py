from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/finwise")
client = MongoClient(MONGO_URI)
db = client.get_default_database()