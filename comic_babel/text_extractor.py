import pytesseract
<<<<<<< HEAD
=======

from comic_babel.config import settings

pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH


>>>>>>> main
def get_text(image) -> str:
    text = pytesseract.image_to_string(image)

    return text
