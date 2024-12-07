import unittest
from pymongo import MongoClient
from unittest.mock import patch
import hashlib
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../integrate_image_recog_backend_mongodb')))

# Import functions to be tested
from inquiry import generate_hash_id, query_product
from range_query import create_index, range_query

class TestQueryAndIndex(unittest.TestCase):
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

    def test_query_product_found(self):
        # Insert a test product
        product = "TestProduct"
        brand = "TestBrand"
        hash_id = generate_hash_id(product, brand)
        self.collection.insert_one({"HashID": hash_id, "Product": product, "Brand": brand})

        with patch("inquiry.collection", self.collection):
            # Perform the query
            with patch("builtins.print") as mocked_print:
                query_product(product, brand)

                # update expectation allow to have _id field
                print_calls = [call.args[0] for call in mocked_print.mock_calls]
                found_call = any(
                    f"'HashID': '{hash_id}'" in call and
                    f"'Product': '{product}'" in call and
                    f"'Brand': '{brand}'" in call
                    for call in print_calls
                )
                self.assertTrue(found_call, f"Expected print call not found for product: {product}, brand: {brand}")

    def test_query_product_not_found(self):
        product = "NonExistentProduct"
        brand = "NonExistentBrand"
        hash_id = generate_hash_id(product, brand)

        with patch("inquiry.collection", self.collection):
            # Perform the query
            with patch("builtins.print") as mocked_print:
                query_product(product, brand)

                # Verify the expected output
                mocked_print.assert_called_with(f"No product found with HashID: {hash_id}")

    def test_create_index(self):
        with patch("range_query.collection", self.collection):
            # Create an index on the 'Product' field
            with patch("builtins.print") as mocked_print:
                create_index("Product")

                # Verify the index exists
                indexes = self.collection.index_information()
                self.assertIn("Product_1", indexes)

                # Verify the expected output
                mocked_print.assert_called_with("Index created: Product_1")

    def test_range_query(self):
    # Insert test products
        product = "TestProduct"
        self.collection.insert_many([
            {"Product": product, "Brand": "BrandA", "Quantity": 10},
            {"Product": product, "Brand": "BrandB", "Quantity": 20},
        ])

        with patch("range_query.collection", self.collection):
            with patch("builtins.print") as mocked_print:
                range_query(product)

                # 调试打印捕获的输出
                print("Captured print calls:", mocked_print.mock_calls)

                # 提取所有打印内容
                print_calls = [
                    call.args[0] for call in mocked_print.mock_calls if len(call.args) > 0
                ]

                # 预期内容
                expected_brand_a = {"Product": "TestProduct", "Brand": "BrandA", "Quantity": 10}
                expected_brand_b = {"Product": "TestProduct", "Brand": "BrandB", "Quantity": 20}

                # 将打印内容解析为字典
                parsed_calls = []
                for call in print_calls:
                    try:
                        # 如果内容是字符串化的字典，使用 eval 转换为字典
                        parsed = eval(call) if isinstance(call, str) else call
                        if "_id" in parsed:
                            del parsed["_id"]  # 忽略 _id 字段
                        parsed_calls.append(parsed)
                    except (SyntaxError, ValueError, TypeError):
                        continue  # 跳过无法解析的内容

                # 检查是否包含预期内容
                self.assertIn(expected_brand_a, parsed_calls, f"Expected BrandA not found: {expected_brand_a}")
                self.assertIn(expected_brand_b, parsed_calls, f"Expected BrandB not found: {expected_brand_b}")


if __name__ == "__main__":
    unittest.main()
