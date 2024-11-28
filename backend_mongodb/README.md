# How to establish MongoDB backend in this project
## Setting Up MongoDB and `pymongo` on Linux

### run setup_mongodb_pymongo.sh
1. Open a terminal.
2. To make the script executable, run:
   ```bash
   chmod +x setup_mongodb_pymongo.sh
3. Execute the script to install MongoDB and pymongo:
    ```bash
    ./setup_mongodb_pymongo.sh
4. Ensure MongoDB is Running. Check the status of the MongoDB service. If MongoDB is running, you should see Active: active (running) in the output.:

    ```bash
    sudo systemctl status mongod
5. Test pymongo. Run the following command to verify that pymongo is installed and working:
    ```bash
    python3 -c "from pymongo import MongoClient; print('pymongo is working')"

## File Usage and Workflow

### 1. Files Overview:
1. **`inventory.csv`**: 
   - Contains the original labeling data used to establish the MongoDB database.

2. **`csv_json_conversion.py`**:
   - Converts `inventory.csv` into a JSON file named `products.json`.

3. **`create_db_with_json.py`**:
   - Uses `products.json` to create a MongoDB database named `inventory_db` and a collection named `products`.

4. **`insert_update_delete.py`**:
   - Provides commands to update the `inventory_db` with any new information recognized by LLM.

---

### 2. Algorithm for Generating Unique ID

- **Hashing Method**:
  - We use the `hashlib.sha256` function to generate a 60-character unique ID for each good.
  - This ID is derived based on the combination of the item's class and brand.
  - The unique ID is used for all CRUD operations in the database.
