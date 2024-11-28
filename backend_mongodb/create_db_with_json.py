# need to pip install pymongo if not installed
from pymongo import MongoClient
import json

# MongoDB configuration
mongo_uri = "mongodb://localhost:27017/"
database_name = "inventory_db"
collection_name = "products"

# read local json file
json_file = "products.json"  
with open(json_file, "r") as file:
    data = json.load(file)  

# connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# insert data from json file
result = collection.insert_many(data)
print(f"Inserted {len(result.inserted_ids)} documents into the '{collection_name}' collection.")

