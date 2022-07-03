from pymongo import MongoClient
import pprint
import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.test_database
collection = db.test_collection
posts = db.posts
db.list_collection_names()
pprint.pprint(posts.find_one())
