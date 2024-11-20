import fitz  # PyMuPDF for PDF handling
from PIL import Image
from transformers import AutoProcessor, AutoModel
import torch

# Initialize Qwen-2 VL model and processor from Hugging Face (replace with actual model if available)
processor = AutoProcessor.from_pretrained("Qwen/Qwen-2-VL")
model = AutoModel.from_pretrained("Qwen/Qwen-2-VL")

# Convert PDF pages to images
def pdf_to_images(pdf_path):
    images = []
    doc = fitz.open(pdf_path)
    for page_num in range(doc.page_count):
        page = doc[page_num]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

# Extract text from images using Qwen-2 VL
def extract_text(images):
    extracted_text = []
    for image in images:
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            output = model(**inputs)
        
        # Process the output to extract text
        extracted_text.append(output)  # Modify this based on actual output format
    return extracted_text

# Save extracted text to a file
def save_text_to_file(text_data, output_file="extracted_text.txt"):
    with open(output_file, "w") as file:
        for page_num, text in enumerate(text_data, 1):
            file.write(f"Page {page_num}:\n{text}\n\n")
    print(f"Text extracted and saved to {output_file}")

# Load PDF, extract text, and save to file
pdf_path = "your_pdf_path_here.pdf"
images = pdf_to_images(pdf_path)
text_data = extract_text(images)
save_text_to_file(text_data, "extracted_text.txt")


"""
