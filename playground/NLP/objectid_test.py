from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
collection = client.TwitterDB["Test IB"]


# result = collection.find_one({"_id": ObjectId('5c5a622fbd234c2c24627f6c')})
# result['_id'] = ObjectId('5c5a622fbd234c2c24627f6d')
# collection.update({'_id': ObjectId('5c5a622fbd234c2c24627f6c')}, {'$set': result})

a = ObjectId("507c7f79bcf86cd7994f6c0e")
print(str(a))

