import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from pymongo import MongoClient
import os
import sys
import hashlib
import tempfile
import shutil

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../integrate_image_recog_backend_mongodb')))

# Now import the required classes and functions
from insert_update_from_image import ProductImageProcessor, generate_hash_id, insert_update_product


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

        cls.image_path = os.path.join(os.path.dirname(__file__), "test_image")

        # Ensure the test image exists in the temporary directory
        assert os.path.exists(cls.image_path), f"Test image not found at: {cls.image_path}"

        # Test processor setup
        cls.model_id = "vikhyatk/moondream2"
        cls.revision = "2024-08-26"
        cls.processor = ProductImageProcessor(cls.model_id, cls.revision, cls.image_path)

    @classmethod
    def tearDownClass(cls):
        # Clean up test database and temporary directory after tests
        cls.client.drop_database(cls.database_name)
        cls.client.close()

    def test_generate_hash_id(self):
        product = "TestProduct"
        brand = "TestBrand"
        hash_id = generate_hash_id(product, brand)
        self.assertEqual(
            hash_id,
            hashlib.sha256(f"{product}{brand}".encode()).hexdigest()
        )

    @patch.object(ProductImageProcessor, '_process_image')
    def test_process_images(self, mock_process_image):
        # Mock the image processing response
        mock_process_image.return_value = {
            "Product": "Laundry detergent",
            "Brand": "Ariel",
            "Quantity": 2
        }

        # Call process_images on the single image
        responses = self.processor.process_images()

        # Assert the mocked response is returned
        self.assertTrue(responses)
        self.assertEqual(len(responses), 1)  # Only one image is processed
        self.assertEqual(responses[0], mock_process_image.return_value)

if __name__ == "__main__":
    unittest.main()
