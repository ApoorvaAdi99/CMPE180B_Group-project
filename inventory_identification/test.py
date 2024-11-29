from PIL import Image

try:
    img = Image.open("inventory_images/Image_20220428_1.jpg")
    img.verify()  # Verify the file integrity
    print("Image is valid!")
except Exception as e:
    print(f"Error processing image: {e}")
