from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from PIL import Image
import os

app = Flask(__name__)
mongo_uri = "mongodb://localhost:27017/"
database_name = "inventory_db"
collection_name = "products"
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    image = request.files['image']
    image_path = os.path.join('inventory_images', image.filename)
    image.save(image_path)
    # Process the image and update the database (pseudo-code)
    # product_details = process_image(image_path)
    # collection.insert_one(product_details)
    return jsonify({'message': 'Image uploaded successfully'})

@app.route('/inventory', methods=['GET'])
def get_inventory():
    products = list(collection.find({}, {'_id': 0}))
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)