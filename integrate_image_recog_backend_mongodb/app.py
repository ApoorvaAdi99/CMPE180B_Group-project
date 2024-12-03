from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
from time import time
from pymongo import MongoClient
import hashlib
from datetime import datetime, timedelta
import os
from flask import Flask, request, render_template

app = Flask(__name__)

class ProductImageProcessor:
    def __init__(self, model_id, revision, inventory_folder):
        self.model_id = model_id
        self.revision = revision
        self.inventory_folder = inventory_folder
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, revision=revision)

    def process_images(self):
        folder_dir = os.path.join(os.curdir, self.inventory_folder)
        results = []
        for image_file in os.listdir(folder_dir):
            if image_file.lower().endswith((".png", ".jpg", ".jpeg")):
                image_path = os.path.join(self.inventory_folder, image_file)
                print(f"Processing image: {image_path}")
                response = self._process_image(image_path)
                if response:
                    results.append(response)
        return results

    def _process_image(self, image_path):
        try:
            image = Image.open(image_path)
            enc_image = self.model.encode_image(image)

            product_type = self._answer_question(
                enc_image,
                "Fill in the blank - Product Type in the picture is  _______."
            )
            product_brand = self._answer_question(
                enc_image,
                "Fill in the blank - Product brand name in the picture is  _______."
            )
            product_quantity = self._answer_question(
                enc_image,
                f"Fill in the blank - Number of {product_brand} in the picture is  _______."
            )

            response = {
                "Product": product_type,
                "Brand": product_brand,
                "Quantity": int(product_quantity),
            }
            print(response)
            return response
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None

    def _answer_question(self, enc_image, question):
        return self.model.answer_question(enc_image, question, self.tokenizer)

# MongoDB Functions
client = MongoClient("mongodb://localhost:27017/")
db = client["inventory_db"]
collection = db["products"]

def generate_hash_id(product, brand):
    unique_string = f"{product}{brand}"
    return hashlib.sha256(unique_string.encode()).hexdigest()

def insert_product(product, brand, quantity, purchase_time, expiration_time):
    hash_id = generate_hash_id(product, brand)
    product_data = {
        "HashID": hash_id,
        "Product": product,
        "Brand": brand,
        "Quantity": quantity,
        "PurchaseTime": purchase_time,
        "ExpirationTime": expiration_time,
    }
    collection.insert_one(product_data)
    print(f"Inserted product: {product_data}")
    return product_data

def get_all_products():
    return list(collection.find())

def update_product(hash_id, product, brand, quantity, purchase_time, expiration_time):
    collection.update_one(
        {"HashID": hash_id},
        {"$set": {
            "Product": product,
            "Brand": brand,
            "Quantity": quantity,
            "PurchaseTime": purchase_time,
            "ExpirationTime": expiration_time,
        }}
    )

def delete_product(hash_id):
    collection.delete_one({"HashID": hash_id})


# Route 1: Page to process images and update database
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        folder_path = request.form.get("folder_path")
        if not folder_path:
            return render_template("index.html", message="Please provide a folder path.")

        start_time = time()
        
        model_id = "vikhyatk/moondream2"
        revision = "2024-08-26"

        processor = ProductImageProcessor(model_id, revision, folder_path)
        responses = processor.process_images()

        inserted_products = []
        for response in responses:
            product = response["Product"]
            brand = response["Brand"]
            quantity = response["Quantity"]
            purchase_time = datetime.now().strftime("%Y-%m-%d")
            expiration_time = (datetime.now() + timedelta(days=730)).strftime("%Y-%m-%d")
            
            inserted_product = insert_product(product, brand, quantity, purchase_time, expiration_time)
            inserted_products.append(inserted_product)

        end_time = time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.2f} seconds")

        return render_template("index.html", message="Images processed and database updated.", products=inserted_products)
    return render_template("index.html")


# Route 2: View Inventory
@app.route("/inventory")
def view_inventory():
    products = get_all_products()
    return render_template("inventory.html", products=products)

# Route 3: Update Inventory
@app.route("/update", methods=["GET", "POST"])
def update_inventory():
    if request.method == "POST":
        hash_id = request.form.get("hash_id")
        product = request.form.get("product")
        brand = request.form.get("brand")
        quantity = int(request.form.get("quantity"))
        purchase_time = request.form.get("purchase_time")
        expiration_time = request.form.get("expiration_time")
        
        update_product(hash_id, product, brand, quantity, purchase_time, expiration_time)
        return redirect(url_for("view_inventory"))
    
    hash_id = request.args.get("hash_id")
    product = collection.find_one({"HashID": hash_id})
    return render_template("update.html", product=product)

# Route 4: Delete Product
@app.route("/delete/<hash_id>")
def delete_product_route(hash_id):
    delete_product(hash_id)
    return redirect(url_for("view_inventory"))

if __name__ == "__main__":
    app.run(debug=True)