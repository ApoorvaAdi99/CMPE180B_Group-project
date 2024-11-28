import csv
import json
import hashlib

# input and output file path
input_csv = "inventory.csv"  
output_json = "products.json"  

# obtain local CSV file
items = []
with open(input_csv, mode="r") as file:
    reader = csv.DictReader(file)  # auto analyze header
    for row in reader:
        product = row["Product"]
        brand = row["Brand"]
        quantity = int(row["Quantity"])  # ensure int for quantity
        purchase_time = row["PurchaseTime"]
        expiration_time = row["ExpirationTime"]

        # genearte HashID based on product name and brand
        hash_id = hashlib.sha256(f"{product}{brand}".encode()).hexdigest()

        # create JSON obj
        items.append({
            "HashID": hash_id,
            "Product": product,
            "Brand": brand,
            "Quantity": quantity,
            "PurchaseTime": purchase_time,
            "ExpirationTime": expiration_time
        })

# save as JSON File
with open(output_json, "w") as file:
    json.dump(items, file, indent=4)

print(f"JSON file '{output_json}' generated successfully!")
