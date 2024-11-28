from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
from time import time
import os

class ProductImageProcessor:
    def __init__(self, model_id, revision, inventory_folder="inventory_images"):
        self.model_id = model_id
        self.revision = revision
        self.inventory_folder = inventory_folder
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, revision=revision)
        self.responses = []

    def process_images(self):
        folder_dir = os.path.join(os.curdir, self.inventory_folder)
        for image_file in os.listdir(folder_dir):
            if image_file.lower().endswith((".png", ".jpg", ".jpeg")):
                image_path = os.path.join(self.inventory_folder, image_file)
                print(f"Processing image: {image_path}")
                response = self._process_image(image_path)
                if response:
                    self.responses.append(response)
        return self.responses

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

            response = ",".join([product_type, product_brand, product_quantity])
            print(response)
            return response
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None

    def _answer_question(self, enc_image, question):
        return self.model.answer_question(enc_image, question, self.tokenizer)

def main():
    start_time = time()
    
    model_id = "vikhyatk/moondream2"
    revision = "2024-08-26"
    #inventory_folder = "inventory_images"

    processor = ProductImageProcessor(model_id, revision)
    responses = processor.process_images()

    end_time = time()
    execution_time = end_time - start_time
    print(f"Moondream Execution time: {execution_time:.2f} seconds")
    print("Responses:")
    for response in responses:
        print(response)

if __name__ == "__main__":
    main()
