import aggdraw
from PIL import Image


def get_drawed_text(size, text, font):
    image = Image.new(mode="RGB", size=size, color=(255, 255, 255))
    drawer = aggdraw.Draw(image)
    drawer.setantialias(True)

    text = text.encode("utf-8")
    drawer.text((0, 0), text, font)
    drawer.flush()
    return image
