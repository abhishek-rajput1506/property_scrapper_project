# from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

class MongoUtil:
    def __init__(self, connection_uri : str):
        self.uri = connection_uri

    def connect_to_remote_database(self):
        client = MongoClient(self.uri, server_api=ServerApi('1'))
                          
        try:
            client.admin.command('ping')
            print("Pinged to deployment. Successfully connected to MongoDB!")
            return client
        except Exception as e:
            print(f"Error in conneting mongodb server : {e}")
            return None

    def get_cursor_for_properties_collection(self):
        mongo_client = self.connect_to_remote_database()
        cursor = None
        if mongo_client:
            try:
                cursor = mongo_client.web_scrapping_data.properties
            except Exception as e:
                print(f"Error in getting properties cursor: {e}")

        return cursor



