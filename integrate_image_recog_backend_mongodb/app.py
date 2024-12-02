from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import os
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["inventory_db"]
collection = db["products"]

# LLM Model setup
model_id = "vikhyatk/moondream2"
revision = "2024-08-26"
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, revision=revision)


# Helper function for hash generation
def generate_hash_id(product, brand):
    unique_string = f"{product}{brand}"
    return hashlib.sha256(unique_string.encode()).hexdigest()


# Helper function to process images
def process_images(folder_path):
    results = []
    for image_file in os.listdir(folder_path):
        if image_file.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(folder_path, image_file)
            try:
                image = Image.open(image_path)
                # Simulate LLM processing
                product = "Sample Product"  # Replace with model logic
                brand = "Sample Brand"  # Replace with model logic
                quantity = 5  # Replace with model logic

                results.append({"Product": product, "Brand": brand, "Quantity": quantity})
            except Exception as e:
                print(f"Error processing {image_file}: {e}")
    return results


# Route 1: Page to process images and update database
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        folder_path = request.form["folder_path"]
        results = process_images(folder_path)

        # Insert results into the database
        for result in results:
            product = result["Product"]
            brand = result["Brand"]
            quantity = result["Quantity"]
            purchase_time = datetime.now().strftime("%Y-%m-%d")
            expiration_time = (datetime.now() + timedelta(days=730)).strftime("%Y-%m-%d")
            hash_id = generate_hash_id(product, brand)
            collection.insert_one({
                "HashID": hash_id,
                "Product": product,
                "Brand": brand,
                "Quantity": quantity,
                "PurchaseTime": purchase_time,
                "ExpirationTime": expiration_time,
            })

        return render_template("index.html", results=results)

    return render_template("index.html")


# Route 2: Page to manually update inventory
@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        product = request.form["product"]
        brand = request.form["brand"]
        quantity = int(request.form["quantity"])
        hash_id = generate_hash_id(product, brand)

        # Update MongoDB
        collection.update_one(
            {"HashID": hash_id},
            {"$set": {"Product": product, "Brand": brand, "Quantity": quantity}},
            upsert=True,
        )

        return redirect(url_for("inventory"))

    return render_template("update.html")


# Route 3: Page to view all inventory
@app.route("/inventory", methods=["GET"])
def inventory():
    items = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB's `_id`
    return render_template("inventory.html", items=items)


if __name__ == "__main__":
    app.run(debug=True)