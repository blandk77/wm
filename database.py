import pymongo
from config import MONGO_URL

class MongoDB:
    def __init__(self, mongo_url):
        self.client = pymongo.MongoClient(mongo_url)
        self.db = self.client["watermark_bot"]
        self.collection = self.db["watermark_urls"]

    def save_watermark_url(self, url, user_id):
        self.collection.update_one({"user_id": user_id}, {"$set": {"url": url}}, upsert=True)

    def get_watermark_url(self, user_id):
        return self.collection.find_one({"user_id": user_id})["url"]

    def remove_watermark_url(self, user_id):
        self.collection.delete_one({"user_id": user_id})
