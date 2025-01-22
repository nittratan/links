import torch
from PIL import Image
import cv2
import docowl

# Load the pre-trained DocOwl model
model = docowl.DocOwlModel.from_pretrained('microsoft/docowl-base')

# Function to preprocess the image
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    pil_image = Image.fromarray(image)
    return pil_image

# Function to extract text from image
def extract_text_from_image(image_path):
    image = preprocess_image(image_path)
    
    # Perform OCR and extraction using DocOwl
    inputs = model.preprocess(image)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Extract detected text
    extracted_text = model.postprocess(outputs)
    
    return extracted_text

# Example usage
image_path = "sample_image.jpg"  # Replace with your image path
extracted_text = extract_text_from_image(image_path)

# Print the extracted text
print("Extracted Text:", extracted_text)
