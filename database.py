import pymongo
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_overlay(user_id, file_id):
    """
    Save overlay image to the database.
    """
    collection.update_one(
        {"user_id": user_id},
        {"$set": {"file_id": file_id}},
        upsert=True
    )

def get_overlay(user_id):
    """
    Retrieve overlay image from the database.
    """
    record = collection.find_one({"user_id": user_id})
    return record["file_id"] if record else None

def remove_overlay(user_id):
    """
    Remove overlay image from the database.
    """
    collection.delete_one({"user_id": user_id})
