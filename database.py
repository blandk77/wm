import pymongo

class MongoDB:
    def __init__(self, mongo_uri):
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client['watermark_bot']
        self.collection = self.db['watermark_urls']

    def save_watermark_url(self, url, chat_id):
        self.collection.insert_one({'chat_id': chat_id, 'url': url})

    def get_watermark_url(self, chat_id):
        return self.collection.find_one({'chat_id': chat_id})['url']
