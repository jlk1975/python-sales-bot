from pymongo import MongoClient
import pprint
import datetime

post = {"author": "JLK",
        "text": "Blog Post 3",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

client = MongoClient('mongodb://localhost:27017/')
db = client.test_database
collection = db.test_collection
db.list_collection_names()
posts = db.posts
post_id = posts.insert_one(post).inserted_id
post_id
# pprint.pprint(posts.find_one())
pprint.pprint(posts.find_one({"author": "Mike"}))
pprint.pprint(posts.find_one({"author": "JLK"}))
