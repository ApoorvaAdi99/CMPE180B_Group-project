# CMPE180B_Group-project - Inventory Management System with Image Recognition and MongoDB Backend

Group Name: DBLegends

Group members:\
Lu Li \
Bhavya Jain \
Apoorva Adimulam \
Nivedita Nair
2 

# Introduction
This project is an information management system built using machine learning with Flask UI, LLM image recognition, and NoSQL (MongoDB) databases. The system processes images to identify products, manages inventory data, and provides CRUD operations for inventory management.

# Project Structure
**Directory:** integrate_image_recog_backend_mongodb
**Files:**
1. app.py \
Main Flask application file.  \
Handles routes for processing images, viewing inventory, updating inventory, deleting products, and uploading JSON files.  \
Contains MongoDB functions for inserting, updating, and deleting products. \
Uses ProductImageProcessor class for image processing.

2. create_db_with_json.py \
Script to create and populate the MongoDB database using a JSON file. \
Drops the existing database and inserts data from products.json. \
Ensures unique index on HashID.

3. csv_json_conversion.py \
Converts inventory.csv into a JSON file named products.json. \
Generates HashID for each product based on its name and brand.

4. insert_update_from_image.py \
Contains the ProductImageProcessor class for processing images. \
Defines MongoDB functions for generating HashID and inserting/updating products. \
Processes images to identify products and update the database.

5. range_query.py \
Script to perform range queries on the MongoDB database. \
Creates an index on the Product field for faster queries. \
Retrieves all items for a specific product. 

6. inquiry.py \
Script to query the MongoDB database for a specific product. \
Generates HashID and retrieves product data based on the hash. 

7. setup_mongodb_pymongo.sh \
Bash script to set up MongoDB and pymongo on a Linux system. \
Installs MongoDB, starts the service, and installs pymongo. 


# Project Setup 
## Prerequisites
Python 3.x \
MongoDB \
Flask \
pymongo library \
transformers library \
PIL library 

## Installation
Clone the repository: \
  git clone https://github.com/yourusername/your-repo.git \
cd your-repo/integrate_image_recog_backend_mongodb

Set up MongoDB and pymongo: \
  chmod +x setup_mongodb_pymongo.sh \
./setup_mongodb_pymongo.sh

Install Python dependencies: \
  pip install -r requirements.txt

# Execution Instructions 
Run the Flask application: \
  python app.py \
  
Access the application: \
  Open a web browser and go to http://localhost:5000.
