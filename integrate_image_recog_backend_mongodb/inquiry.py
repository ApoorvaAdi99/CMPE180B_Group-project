import hashlib
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["inventory_db"]
collection = db["products"]

def generate_hash_id(product, brand):
    unique_string = f"{product}{brand}"
    return hashlib.sha256(unique_string.encode()).hexdigest()

# Query operation
def query_product(product, brand):
    hash_id = generate_hash_id(product, brand)
    query_filter = {"HashID": hash_id}
    product_data = collection.find_one(query_filter)
    if product_data:
        print(f"Found product: {product_data}")
    else:
        print(f"No product found with HashID: {hash_id}")

print("\n--- Query Operation After Insert ---")
query_product("Oil", "Rg")