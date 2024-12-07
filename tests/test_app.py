# test_app.py

import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import from the app module
from integrate_image_recog_backend_mongodb.app import (
    app,
    generate_hash_id,
    insert_product,
    update_product,
    delete_product
)

class TestInventoryManagementSystem(unittest.TestCase):
    def setUp(self):
        """Set up test client and test database"""
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Mock MongoDB collection
        self.patcher = patch('integrate_image_recog_backend_mongodb.app.collection')
        self.mock_collection = self.patcher.start()

    def tearDown(self):
        """Clean up after tests"""
        self.patcher.stop()

    # Route Tests
    def test_index_get(self):
        """Test GET request to index page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Inventory Management System', response.data)

    def test_index_post_without_folder(self):
        """Test POST request to index without folder path"""
        response = self.client.post('/', data={})
        self.assertIn(b'Please provide a folder path', response.data)

    def test_view_inventory(self):
        """Test inventory view route"""
        self.mock_collection.find.return_value = [
            {"Product": "Test", "Brand": "TestBrand", "Quantity": 1}
        ]
        response = self.client.get('/inventory')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Inventory', response.data)

    # Database Operation Tests
    def test_generate_hash_id(self):
        """Test hash ID generation"""
        hash_id = generate_hash_id("TestProduct", "TestBrand")
        self.assertIsInstance(hash_id, str)
        self.assertTrue(len(hash_id) > 0)

    def test_insert_product(self):
        """Test product insertion"""
        product_data = {
            "product": "Test",
            "brand": "TestBrand",
            "quantity": 1,
            "purchase_time": datetime.now().strftime("%Y-%m-%d"),
            "expiration_time": datetime.now().strftime("%Y-%m-%d")
        }
        # Mock find_one to return None (product doesn't exist)
        self.mock_collection.find_one.return_value = None

        insert_product(**product_data)

        self.mock_collection.find_one.assert_called_once_with({
            "HashID": generate_hash_id("Test", "TestBrand")
        })
        self.mock_collection.insert_one.assert_called_once()

    def test_update_product(self):
        """Test product update"""
        product_data = {
            "hash_id": "test_hash",
            "product": "Test",
            "brand": "TestBrand",
            "quantity": 1,
            "purchase_time": datetime.now().strftime("%Y-%m-%d"),
            "expiration_time": datetime.now().strftime("%Y-%m-%d")
        }
        update_product(**product_data)
        self.mock_collection.find_one.assert_called_once()

    def test_delete_product(self):
        """Test product deletion"""
        delete_product("test_hash")
        self.mock_collection.delete_one.assert_called_once_with(
            {"HashID": "test_hash"}
        )

    # Form Submission Tests
    def test_update_form_submission(self):
        """Test update form submission"""
        test_data = {
            'hash_id': 'test_hash',
            'product': 'TestProduct',
            'brand': 'TestBrand',
            'quantity': '5',
            'purchase_time': '2024-03-20',
            'expiration_time': '2026-03-20'
        }
        response = self.client.post('/update', data=test_data)
        self.assertEqual(response.status_code, 302)  # Redirect after update

if __name__ == '__main__':
    unittest.main()