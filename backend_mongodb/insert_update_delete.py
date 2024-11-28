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

# Insert operation
def insert_product(product, brand, quantity, purchase_time, expiration_time):
    hash_id = generate_hash_id(product, brand)
    product_data = {
        "HashID": hash_id,
        "Product": product,
        "Brand": brand,
        "Quantity": quantity,
        "PurchaseTime": purchase_time,
        "ExpirationTime": expiration_time,
    }
    collection.insert_one(product_data)
    print(f"Inserted product: {product_data}")

# Update operation
def update_product(product, brand, updated_fields):
    hash_id = generate_hash_id(product, brand)
    update_filter = {"HashID": hash_id}
    update_values = {"$set": updated_fields}
    collection.update_one(update_filter, update_values)
    print(f"Updated product with HashID: {hash_id}")

# Delete operation
def delete_product(product, brand):
    hash_id = generate_hash_id(product, brand)
    delete_filter = {"HashID": hash_id}
    result = collection.delete_one(delete_filter)
    if result.deleted_count > 0:
        print(f"Deleted product with HashID: {hash_id}")
    else:
        print(f"No product found with HashID: {hash_id}")

# Query operation
def query_product(product, brand):
    hash_id = generate_hash_id(product, brand)
    query_filter = {"HashID": hash_id}
    product_data = collection.find_one(query_filter)
    if product_data:
        print(f"Found product: {product_data}")
    else:
        print(f"No product found with HashID: {hash_id}")

# Example usage
print("\n--- Insert Operation ---")
insert_product("Juice", "Boost", 1, "2024-11-21", "2026-11-21")

print("\n--- Query Operation After Insert ---")
query_product("Juice", "Boost")

print("\n--- Update Operation ---")
update_product("Juice", "Boost", {"Quantity": 10})

print("\n--- Query Operation After Update ---")
query_product("Juice", "Boost")

print("\n--- Delete Operation ---")
delete_product("Juice", "Boost")

print("\n--- Query Operation After Delete ---")
query_product("Juice", "Boost")
