from pymongo import MongoClient

# MongoDB configuration
mongo_uri = "mongodb://localhost:27017/"
database_name = "inventory_db"
collection_name = "products"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Create an index on the 'Product' field
print("Creating an index on the 'Product' field...")
index_name = collection.create_index("Product")

# Print the name of the created index
print(f"Index created: {index_name}")

# Verify all indexes on the collection
indexes = collection.index_information()
print("\nCurrent Indexes:")
for name, details in indexes.items():
    print(f"Index Name: {name}, Details: {details}")
