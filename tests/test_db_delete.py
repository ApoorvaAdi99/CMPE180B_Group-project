import unittest
from unittest.mock import patch
from pymongo import MongoClient
import hashlib
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../integrate_image_recog_backend_mongodb')))

# Import functions to be tested
from delete_op import generate_hash_id, delete_product

class TestDeleteProduct(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # MongoDB test configuration
        cls.mongo_uri = "mongodb://localhost:27017/"
        cls.database_name = "test_inventory_db"
        cls.client = MongoClient(cls.mongo_uri)
        cls.db = cls.client[cls.database_name]
        cls.collection = cls.db["products"]

    @classmethod
    def tearDownClass(cls):
        # Clean up the test database
        cls.client.drop_database(cls.database_name)
        cls.client.close()

    def setUp(self):
        # Clear the collection before each test
        self.collection.delete_many({})

    def test_generate_hash_id(self):
        product = "TestProduct"
        brand = "TestBrand"
        expected_hash_id = hashlib.sha256(f"{product}{brand}".encode()).hexdigest()
        actual_hash_id = generate_hash_id(product, brand)
        self.assertEqual(actual_hash_id, expected_hash_id, "Hash ID generation failed.")

    def test_delete_product_success(self):
        # Insert a test product
        product = "TestProduct"
        brand = "TestBrand"
        hash_id = generate_hash_id(product, brand)
        self.collection.insert_one({"HashID": hash_id, "Product": product, "Brand": brand})

        with patch("delete_op.collection", self.collection):
            with patch("builtins.print") as mocked_print:
                delete_product(product, brand)

                # Verify deletion
                deleted_product = self.collection.find_one({"HashID": hash_id})
                self.assertIsNone(deleted_product, "Product was not deleted.")
                mocked_print.assert_called_with(f"Deleted product with HashID: {hash_id}")

    def test_delete_product_not_found(self):
        product = "NonExistentProduct"
        brand = "NonExistentBrand"
        hash_id = generate_hash_id(product, brand)

        with patch("delete_op.collection", self.collection):
            with patch("builtins.print") as mocked_print:
                delete_product(product, brand)

                # Verify no product was deleted
                mocked_print.assert_called_with(f"No product found with HashID: {hash_id}")

if __name__ == "__main__":
    unittest.main()
