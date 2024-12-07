import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from pymongo import MongoClient
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../integrate_image_recog_backend_mongodb')))

# Import required classes and functions
from insert_update_from_image import ProductImageProcessor, generate_hash_id, insert_update_product, main


class TestProductImageProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # MongoDB test configuration
        cls.mongo_uri = "mongodb://localhost:27017/"
        cls.database_name = "test_inventory_db"
        cls.client = MongoClient(cls.mongo_uri)
        cls.client.drop_database(cls.database_name)
        cls.db = cls.client[cls.database_name]
        cls.collection = cls.db["products"]

    @classmethod
    def tearDownClass(cls):
        # Clean up test database
        cls.client.drop_database(cls.database_name)
        cls.client.close()

    def setUp(self):
        # Clear the collection before each test
        self.collection.delete_many({})

    @patch("insert_update_from_image.collection", new_callable=lambda: None)
    def test_insert_new_product(self, mock_collection):
        # Replace the global `collection` in the main code with the test collection
        with patch("insert_update_from_image.collection", self.collection):
            # Test inserting a new product
            product = "TestProduct"
            brand = "TestBrand"
            quantity = 10
            purchase_time = datetime.now().strftime("%Y-%m-%d")
            expiration_time = (datetime.now() + timedelta(days=730)).strftime("%Y-%m-%d")

            insert_update_product(product, brand, quantity, purchase_time, expiration_time)

            # Verify the product is inserted
            inserted_product = self.collection.find_one({"HashID": generate_hash_id(product, brand)})
            self.assertIsNotNone(inserted_product, f"Product {product} was not inserted")
            self.assertEqual(inserted_product["Product"], product)
            self.assertEqual(inserted_product["Brand"], brand)
            self.assertEqual(inserted_product["Quantity"], quantity)
            self.assertEqual(len(inserted_product["Batches"]), 1)
            self.assertEqual(inserted_product["Batches"][0]["Quantity"], quantity)

    @patch("insert_update_from_image.collection", new_callable=lambda: None)
    def test_update_existing_product(self, mock_collection):
        # Replace the global `collection` in the main code with the test collection
        with patch("insert_update_from_image.collection", self.collection):
            # Insert an existing product
            product = "ExistingProduct"
            brand = "ExistingBrand"
            initial_quantity = 10
            purchase_time = datetime.now().strftime("%Y-%m-%d")
            expiration_time = (datetime.now() + timedelta(days=730)).strftime("%Y-%m-%d")

            insert_update_product(product, brand, initial_quantity, purchase_time, expiration_time)

            # Update the same product
            additional_quantity = 5
            insert_update_product(product, brand, additional_quantity, purchase_time, expiration_time)

            # Verify the product is updated
            updated_product = self.collection.find_one({"HashID": generate_hash_id(product, brand)})
            self.assertIsNotNone(updated_product, f"Product {product} was not updated")
            self.assertEqual(updated_product["Quantity"], initial_quantity + additional_quantity)
            self.assertEqual(len(updated_product["Batches"]), 2)
            self.assertEqual(updated_product["Batches"][-1]["Quantity"], additional_quantity)

    @patch("insert_update_from_image.collection", new_callable=lambda: None)
    @patch("insert_update_from_image.ProductImageProcessor.process_images")
    def test_main_function(self, mock_process_images, mock_collection):
        # Replace the global `collection` in the main code with the test collection
        with patch("insert_update_from_image.collection", self.collection):
            # Mock the responses from process_images
            mock_process_images.return_value = [
                {"Product": "MockProduct1", "Brand": "MockBrand1", "Quantity": 10},
                {"Product": "MockProduct2", "Brand": "MockBrand2", "Quantity": 5},
            ]

            # Run the main function
            main()

            # Verify the products are inserted
            product1 = self.collection.find_one({"HashID": generate_hash_id("MockProduct1", "MockBrand1")})
            product2 = self.collection.find_one({"HashID": generate_hash_id("MockProduct2", "MockBrand2")})
            self.assertIsNotNone(product1, "MockProduct1 was not inserted")
            self.assertIsNotNone(product2, "MockProduct2 was not inserted")
            self.assertEqual(product1["Quantity"], 10)
            self.assertEqual(product2["Quantity"], 5)


if __name__ == "__main__":
    unittest.main()
