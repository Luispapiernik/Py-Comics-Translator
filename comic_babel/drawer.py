import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def write_text(size, text):
    pil_image = Image.fromarray(image)
    pil_image = Image.new(image)
    drawer = ImageDraw.Draw(pil_image)
    font = ImageFont.truetype("Roboto-Regular.ttf", 50)
    drawer.text((0, 0), "Your Text Here", font=font)
    image = np.asarray(pil_image)
    return image
