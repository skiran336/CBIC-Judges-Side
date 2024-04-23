# mongo_utils.py
from pymongo import MongoClient
import os

def get_mongo_client():
    mongo_uri = os.getenv("MONGO_URI", "your_default_mongo_uri")
    return MongoClient(mongo_uri)

def get_collection(collection_name):
    client = get_mongo_client()
    db = client.get_default_database()  # Make sure your MONGO_URI includes the DB name or specify here explicitly
    return db[collection_name]
