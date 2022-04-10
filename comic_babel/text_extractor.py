import pytesseract

TESSERACT_PATH = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def get_text(image):
    text = pytesseract.image_to_string(image)

    return text
