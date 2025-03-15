import pymongo

class MongoDB:
    def __init__(self, mongo_uri, db_name, collection_name):
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def add_overlay_image(self, user_id, overlay_image):
        self.collection.update_one({"user_id": user_id}, {"$set": {"overlay_image": overlay_image}}, upsert=True)

    def get_overlay_image(self, user_id):
        user_data = self.collection.find_one({"user_id": user_id})
        if user_data:
            return user_data["overlay_image"]
        return None
