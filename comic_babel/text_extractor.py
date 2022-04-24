import platform

import numpy as np
import pytesseract

from comic_babel.config import settings

if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH


def get_text(image: np.ndarray) -> str:
    text = pytesseract.image_to_string(image)

    return text
