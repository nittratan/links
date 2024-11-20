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
Handles the upload of data files for procest

This endpoint allows users to upload data files, typically containing claim adjustment details. 
The uploaded file is validated for format and content compliance before being processed. 
If the upload is successful, the data is either queued for further processing or 
immediately integrated into the system.

### Features:
- Accepts file uploads in specified formats (e.g., CSV, Excel).
- Validates the structure and content of the file.
- Logs upload details for auditing purposes.
- Returns appropriate error messages for invalid or failed uploads.

### Request:
- **Method**: POST
- **Headers**: `Content-Type: multipart/form-data`
- **Body**: 
    - `file` (required): The data file to upload.
    - Additional optional metadata if required.

### Response:
- **200 OK**: File successfully uploaded and queued/processed.
- **400 Bad Request**: Invalid file format or missing required fields.
- **500 Internal Server Error**: An unexpected error occurred.

### Example Usage:
```curl
curl -X POST "https://api.example.com/uploadData" \
-H "Authorization: Bearer <token>" \
-F "file=@adjustment_data.csv"
