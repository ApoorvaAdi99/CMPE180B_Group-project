
# CMPE180B Group Project - Inventory Management System with Image Recognition and MongoDB Backend

**Group Name:** DBLegends  
**Group Members:**  
- Lu Li  
- Bhavya Jain  
- Apoorva Adimulam  
- Nivedita Nair  

---

## Introduction

The Inventory Management System leverages machine learning, Flask for the user interface, LLM-based image recognition, and MongoDB as a NoSQL database. This system processes images to identify products, manages inventory data, and provides comprehensive CRUD operations for inventory management.

---

## Project Structure

### **Directory**: `integrate_image_recog_backend_mongodb`

### **Files:**

1. **`app.py`**  
   - Main Flask application file.  
   - Handles routes for processing images, viewing inventory, updating inventory, deleting products, and uploading JSON files.  
   - Contains MongoDB functions for inserting, updating, and deleting products.  
   - Uses the `ProductImageProcessor` class for image processing.

2. **`create_db_with_json.py`**  
   - Script to create and populate the MongoDB database using a JSON file.  
   - Drops the existing database and inserts data from `products.json`.  
   - Ensures unique indexing on `HashID`.  
   - Creates initial batches for every unique product.

3. **`csv_json_conversion.py`**  
   - Converts `inventory.csv` into a JSON file named `products.json`.  
   - Generates `HashID` for each product based on its name and brand.

4. **`insert_update_from_image.py`**  
   - Contains the `ProductImageProcessor` class for processing images.  
   - Defines MongoDB functions for generating `HashID` and inserting/updating products.  
   - Processes images to identify products and update the database.  
   - Adds new batches to existing products or inserts new records for products not found in the database.  
   - Supports timestamp-based batch tracking.

5. **`delete_op.py`**  
   - Contains the `delete_product` function for deleting records from the database using a combination of product and type.

6. **`range_query.py`**  
   - Script to perform range queries on the MongoDB database.  
   - Creates an index on the `Product` field for faster queries.  
   - Retrieves all items for a specific product.

7. **`inquiry.py`**  
   - Script to query the MongoDB database for a specific product.  
   - Generates `HashID` and retrieves product data based on the hash.

8. **`dependencies/setup_mongodb_pymongo.sh`**  
   - Bash script to set up MongoDB and `pymongo` on a Linux system.  
   - Installs MongoDB, starts the service, and installs `pymongo`.

9. **`dependencies/LLM_dependencies.sh`**  
   - Bash script to set up LLM dependencies on a Linux system.  
   - Installs `transformers`, `torch` (GPU support version), and `einops`.

10. **`dependencies/frontend.sh`**  
    - Bash script to set up frontend dependencies.  
    - Installs Flask.

---

## Project Setup

### **Prerequisites**

- Python 3.x  
- MongoDB  
- Flask  
- `pymongo` library  
- `transformers` library  
- `Pillow` (PIL) library  

### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/luliCloud/CMPE180B_Group-project.git
   cd CMPE180B_group-project/integrate_image_recog_backend_mongodb
   ```

2. Set up dependencies:
   ```bash
   chmod +x dependencies/setup_mongodb_pymongo.sh
   ./dependencies/setup_mongodb_pymongo.sh

   chmod +x dependencies/frontend.sh
   ./dependencies/frontend.sh

   chmod +x dependencies/LLM_dependencies.sh
   ./dependencies/LLM_dependencies.sh
   ```

---

## Tests

Rigorous tests have been written for all key components of the inventory management system.

### **Directory**: `tests`

### **Files:**

1. **`test_app.py`**  
   - Tests all functions in `app.py`, including database creation and CRUD operations.

2. **`test_db_creation.py`**  
   - Tests all functions in `create_db_with_json.py`.  
   - Verifies normal database creation.

3. **`test_db_delete.py`**  
   - Tests the `delete_product` function in `delete_op.py`.  
   - Verifies records can be deleted using product and type.

4. **`test_image_process.py`**  
   - Tests image processing functions in `insert_update_from_image.py`.  
   - Verifies uploaded images can be found in the target directory, and their information is properly recognized and extracted by LLM.

5. **`test_insert_update.py`**  
   - Tests insert and update functions in `insert_update_from_image.py`.  
   - Verifies extracted information is inserted or updated in the database accordingly.

6. **`test_query_range_index.py`**  
   - Tests `range_query.py` and `inquiry.py`.  
   - Verifies second indexes can be created, and both precise and range queries work as expected.

---

## Execution Instructions

### **Run with the UI**

1. Start the Flask application:
   ```bash
   python app.py
   ```
2. Access the application in a web browser:
   ```
   http://localhost:5000
   ```

### **Run with the Backend**

1. Create the database using a JSON file:
   ```bash
   python3 create_db_with_json.py
   ```

2. Insert and update information from newly scanned images:
   ```bash
   python3 insert_update_from_image.py
   ```

3. Delete records from the database:
   ```bash
   python3 delete_op.py
   ```

4. Perform precise queries:
   ```bash
   python3 inquiry.py
   ```

5. Perform range queries:
   ```bash
   python3 range_query.py
   ```

6. Create second indexes:
   ```bash
   python3 range_query.py
   ```
