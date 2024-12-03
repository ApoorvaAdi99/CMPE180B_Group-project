from pymongo import MongoClient

# MongoDB configuration
mongo_uri = "mongodb://localhost:27017/"
database_name = "inventory_db"
collection_name = "products"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

def create_index(field_name):
    """Create an index on the specified field."""
    print(f"Creating an index on the '{field_name}' field...")
    index_name = collection.create_index(field_name)
    print(f"Index created: {index_name}")

def range_query(product_name):
    """
    Perform a range query on the 'Product' field to find all items for a specific product.
    This query retrieves all brands and their details for the given product.
    """
    print(f"Performing range query for Product: {product_name}")
    query = {"Product": product_name}
    results = collection.find(query)
    
    # Count the number of matching documents
    count = collection.count_documents(query)
    
    if count > 0:
        print(f"Found {count} items for Product: {product_name}")
        for item in results:
            print(item)
    else:
        print(f"No items found for Product: {product_name}")

def main():
    # Create a secondary index on 'Product' for faster range queries
    create_index("Product")
    
    # Perform a range query on 'Product'
    product_name = input("Enter the Product name for range query: ")
    range_query(product_name)

if __name__ == "__main__":
    main()
