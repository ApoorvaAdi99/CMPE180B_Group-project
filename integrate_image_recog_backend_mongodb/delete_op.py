import hashlib
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["inventory_db"]
collection = db["products"]

# Function to generate HashID based on Product and Brand
def generate_hash_id(product, brand):
    unique_string = f"{product}{brand}"
    return hashlib.sha256(unique_string.encode()).hexdigest()

# Delete operation
def delete_product(product, brand):
    hash_id = generate_hash_id(product, brand)
    delete_filter = {"HashID": hash_id}
    result = collection.delete_one(delete_filter)
    if result.deleted_count > 0:
        print(f"Deleted product with HashID: {hash_id}")
    else:
        print(f"No product found with HashID: {hash_id}")