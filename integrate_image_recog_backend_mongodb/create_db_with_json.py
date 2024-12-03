# # need to pip install pymongo if not installed
# from pymongo import MongoClient
# import json

# # MongoDB configuration
# mongo_uri = "mongodb://localhost:27017/"
# database_name = "inventory_db"
# collection_name = "products"

# # read local json file
# json_file = "products.json"  
# with open(json_file, "r") as file:
#     data = json.load(file)  

# # connect to MongoDB
# client = MongoClient(mongo_uri)
# db = client[database_name]
# collection = db[collection_name]

# # insert data from json file
# result = collection.insert_many(data)
# print(f"Inserted {len(result.inserted_ids)} documents into the '{collection_name}' collection.")

# need to pip install pymongo if not installed
from pymongo import MongoClient
import json
from datetime import datetime, timedelta
import hashlib

# MongoDB configuration
mongo_uri = "mongodb://localhost:27017/"
database_name = "inventory_db"
collection_name = "products"

# Function to generate HashID based on Product and Brand
def generate_hash_id(product, brand):
    unique_string = f"{product}{brand}"
    return hashlib.sha256(unique_string.encode()).hexdigest()

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Drop existing database to reset
print(f"Dropping database: {database_name}...")
client.drop_database(database_name)
print(f"Database '{database_name}' dropped successfully.")

# Read local JSON file
json_file = "products.json"  
with open(json_file, "r") as file:
    data = json.load(file)  

# Insert data into MongoDB as the first batch
for item in data:
    product = item["Product"]
    brand = item["Brand"]
    quantity = item["Quantity"]
    purchase_time = item["PurchaseTime"]
    expiration_time = item["ExpirationTime"]

    hash_id = generate_hash_id(product, brand)

    # Create the document structure for the first batch
    document = {
        "HashID": hash_id,
        "Product": product,
        "Brand": brand,
        "Quantity": quantity,
        "Batches": [
            {
                "Quantity": quantity,
                "PurchaseTime": purchase_time,
                "ExpirationTime": expiration_time
            }
        ]
    }

    # Insert the document into the collection
    collection.insert_one(document)

print(f"Inserted {len(data)} documents into the '{collection_name}' collection.")

