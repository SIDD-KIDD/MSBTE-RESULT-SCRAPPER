import pytesseract
from PIL import Image

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def convert_to_bw(image_path, threshold):
    # Open the image
    with Image.open(image_path) as img:
        # Convert the image to grayscale
        bw_img = img.convert('L')
        # Apply threshold to convert to black and white
        bw_img = bw_img.point(lambda x: 0 if x < threshold else 255, '1')
        # Save the black and white image
        bw_img.save("bw.png")
        return "bw.png"

def ocr_image(image_path):
    # Convert the image to black and white with increased threshold
    bw_image_path = convert_to_bw(image_path, threshold=200)  # Adjust threshold as needed
    
    # Open the black and white image
    with Image.open(bw_image_path) as img:
        # Perform OCR
        text = pytesseract.image_to_string(img)
        return text

if __name__ == "__main__":
    # Path to the original image file
    image_path = "bw2.png"
    
    # Perform OCR on the black and white image with increased threshold
    text = ocr_image(image_path)
    
    # Print the extracted text
    print("Extracted Text from black and white image:")
    print(text)
