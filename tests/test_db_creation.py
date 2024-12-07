# test for create_db_with_json.py

import unittest
from pymongo import MongoClient
from datetime import datetime
import hashlib

# MongoDB configuration
mongo_uri = "mongodb://localhost:27017/"
database_name = "inventory_db"
products_collection = "products"
orders_collection = "orders"
locations_collection = "locations"

# Function to generate HashID based on Product and Brand
def generate_hash_id(product, brand):
    unique_string = f"{product}{brand}"
    return hashlib.sha256(unique_string.encode()).hexdigest()

class TestDatabaseCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Connect to MongoDB and set up collections
        cls.client = MongoClient(mongo_uri)
        cls.db = cls.client[database_name]

    @classmethod
    def tearDownClass(cls):
        # Drop the database after all tests
        cls.client.drop_database(database_name)
        cls.client.close()

    def test_collections_created(self):
        # Check that the expected collections are created
        collections = self.db.list_collection_names()
        expected_collections = [products_collection, orders_collection, locations_collection]
        self.assertCountEqual(collections, expected_collections)

    def test_products_data(self):
        # Verify that products collection has documents with correct structure
        products = list(self.db[products_collection].find())
        self.assertGreater(len(products), 0, "Products collection is empty.")
        for product in products:
            self.assertIn("HashID", product)
            self.assertIn("Product", product)
            self.assertIn("Brand", product)
            self.assertIn("Quantity", product)
            self.assertIn("Batches", product)
            self.assertIsInstance(product["Batches"], list)
            for batch in product["Batches"]:
                self.assertIn("Quantity", batch)
                self.assertIn("PurchaseTime", batch)
                self.assertIn("ExpirationTime", batch)

    def test_orders_data(self):
        # Verify that orders collection has documents with correct structure
        orders = list(self.db[orders_collection].find())
        self.assertGreater(len(orders), 0, "Orders collection is empty.")
        for order in orders:
            self.assertIn("OrderID", order)
            self.assertIn("OrderDate", order)
            self.assertIn("HashID", order)
            self.assertIn("Quantity", order)
            self.assertIn("Status", order)
            # Verify that OrderDate is a valid datetime string
            datetime.strptime(order["OrderDate"], '%Y-%m-%d %H:%M:%S')

    def test_locations_data(self):
        # Verify that locations collection has documents with correct structure
        locations = list(self.db[locations_collection].find())
        self.assertGreater(len(locations), 0, "Locations collection is empty.")
        for location in locations:
            self.assertIn("LocationID", location)
            self.assertIn("WarehouseName", location)
            self.assertIn("Address", location)
            self.assertIn("Capacity", location)
            self.assertIsInstance(location["Capacity"], int)

if __name__ == "__main__":
    unittest.main()

# expect output
# 
# Ran 4 tests in 0.015s

# OK