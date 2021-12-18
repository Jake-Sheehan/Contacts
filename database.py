from pymongo import MongoClient


class Database:

    def __init__(self):
        # Connects to cloud database
        self.client = MongoClient(
            "mongodb+srv://jake-sheehan:snhu2021"
            "@cluster0.6q4yf.mongodb.net/contacts?retryWrites=true&w=majority")
        # Grab the database
        self.db = self.client.contacts
        # Grab the collection
        self.collection = self.db.default

    def insert(self, contact):
        self.collection.insert_one(contact)

    def delete(self, contact):
        self.collection.delete_one(contact)
