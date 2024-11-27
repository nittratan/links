from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image

def extract_text_with_nvlm(image_path):
    """
    Extract text from an image using NVIDIA's Donut NVLM model.
    
    Args:
        image_path (str): Path to the input image.
    
    Returns:
        str: Extracted text.
    """
    # Load NVIDIA's Donut processor and model
    processor = DonutProcessor.from_pretrained("nvidia/donut-base")
    model = VisionEncoderDecoderModel.from_pretrained("nvidia/donut-base")
    
    # Open and preprocess the image
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(image, return_tensors="pt").pixel_values
    
    # Generate text
    outputs = model.generate(pixel_values)
    text = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    
    return text


# Example usage
if __name__ == "__main__":
    image_path = "path/to/your/image.jpg"
    text = extract_text_with_nvlm(image_path)
    print("Extracted Text:", text)
