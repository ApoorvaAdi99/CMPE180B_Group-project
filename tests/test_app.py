# test_app.py

import unittest
from app import app, ProductImageProcessor, generate_hash_id, insert_product, update_product, delete_product
from unittest.mock import patch, MagicMock
from datetime import datetime
import os

class TestInventoryManagementSystem(unittest.TestCase):
    def setUp(self):
        """Set up test client and test database"""
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Mock MongoDB connection
        self.patcher = patch('app.collection')
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

    @patch('app.ProductImageProcessor')
    def test_index_post_with_folder(self, mock_processor):
        """Test POST request to index with folder path"""
        mock_processor.return_value.process_images.return_value = [
            {"Product": "Test", "Brand": "TestBrand", "Quantity": 1}
        ]
        response = self.client.post('/', data={'folder_path': 'test_folder'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Images processed', response.data)

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
            "Product": "Test",
            "Brand": "TestBrand",
            "Quantity": 1,
            "PurchaseTime": datetime.now().strftime("%Y-%m-%d"),
            "ExpirationTime": datetime.now().strftime("%Y-%m-%d")
        }
        insert_product(**product_data)
        self.mock_collection.find_one.assert_called_once()
        self.assertTrue(
            self.mock_collection.insert_one.called or 
            self.mock_collection.update_one.called
        )

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

    # Image Processing Tests
    @patch('PIL.Image.open')
    def test_process_image(self, mock_image_open):
        """Test image processing"""
        mock_image = MagicMock()
        mock_image_open.return_value = mock_image
        
        processor = ProductImageProcessor(
            model_id="test_model",
            revision="test_revision",
            inventory_folder="test_folder"
        )
        
        # Mock the model's methods
        processor.model.encode_image = MagicMock(return_value="encoded_image")
        processor.model.answer_question = MagicMock(return_value="test_answer")
        
        response = processor._process_image("test_image.jpg")
        self.assertIsNotNone(response)
        self.assertIn("Product", response)
        self.assertIn("Brand", response)
        self.assertIn("Quantity", response)

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

    def test_invalid_form_submission(self):
        """Test form submission with invalid data"""
        test_data = {
            'hash_id': 'test_hash',
            'product': 'TestProduct',
            'brand': 'TestBrand',
            'quantity': 'invalid',  # Invalid quantity
            'purchase_time': '2024-03-20',
            'expiration_time': '2026-03-20'
        }
        response = self.client.post('/update', data=test_data)
        self.assertNotEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()