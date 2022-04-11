import pytesseract
def get_text(image) -> str:
    text = pytesseract.image_to_string(image)

    return text
