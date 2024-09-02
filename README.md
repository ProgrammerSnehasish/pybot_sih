# pybot_sih
import cv2
import pytesseract
import difflib
import os
import csv

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'  # Update this path if necessary

def extract_text_from_image(image_path):
    try:
        img = cv2.imread(image_path)

        # Check if the image was loaded successfully
        if img is None:
            raise FileNotFoundError(f"Image file '{image_path}' not found or cannot be opened.")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray)

        return text

    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None

def compare_text_with_csv(extracted_text, csv_file_path):
    try:
        # Read the CSV file content as a single string
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            csv_content = '\n'.join([','.join(row) for row in reader])

        differences = difflib.unified_diff(csv_content.splitlines(), extracted_text.splitlines())

        # Display the differences
        for line in differences:
            print(line)

    except Exception as e:
        print(f"Error comparing text with CSV file: {e}")

# Example usage
image_path = 'image_with_text.png'  # Replace with the path to your image
csv_file_path = 'example.csv'       # Replace with the path to your CSV file

# Extract text from the image
extracted_text = extract_text_from_image(image_path)
if extracted_text:
    print("Extracted Text:", extracted_text)

    # Compare with the CSV file
    compare_text_with_csv(extracted_text, csv_file_path)
