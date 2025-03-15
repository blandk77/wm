import pymongo
from config import MONGO_COLLECTION_NAME, MONGO_DB_NAME, MONGO_URL
class MongoDB:
    def __init__(self, mongo_uri, db_name, collection_name):
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def add_overlay_image(self, overlay_image):
        self.collection.insert_one({"overlay_image": overlay_image})

    def remove_overlay_image(self):
        self.collection.delete_many({})

    def get_overlay_image(self):
        overlay_image = self.collection.find_one({"overlay_image": {"$exists": True}})
        if overlay_image:
            return overlay_image["overlay_image"]
        return None
