from PIL import Image, ImageDraw


def get_drawed_text(size, text):
    image = Image.new(mode="RGB", size=size, color=(255, 255, 255))
    drawer = ImageDraw.Draw(image)

    text = text.encode("utf-8")
    drawer.text((0, 0), text, fill=(0, 0, 0))
    return image
