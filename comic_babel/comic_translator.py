import os
import re

import aggdraw
from PIL import Image, ImageChops

import comic_babel.utils.image_utils as imgutils
from comic_babel.drawer import get_drawed_text
from comic_babel.segmenter_model import segment_image
from comic_babel.text_detector import detect_text
from comic_babel.text_extractor import get_text
from comic_babel.translator import translate


class ComicTranslator:
    """
    Class with all translating process of the comic specified.

    TODO: remember recursiveness reading the images to be translated

    Parameters
    ------------
    input_folder: str
    ouput_folder: str
    filename_regex: str
    """

    def __init__(
        self, *, input_folder: str, output_folder: str, filename_regex: str,
        font_path: str,
    ) -> None:
        self.font = aggdraw.Font((0, 0, 0), font_path, 12)
        # get valid paths for the images files
        valid_paths = [
            filename
            for filename in os.listdir(input_folder)
            if (
                re.fullmatch(filename_regex, filename)
                and imgutils.is_img_file(os.path.join(input_folder, filename))
            )
        ]

        # get the complete path to the image input and output
        self.input_paths = [
            os.path.join(input_folder, filename)
            for filename in valid_paths
        ]
        self.output_paths = [
            os.path.join(output_folder, filename)
            for filename in valid_paths
        ]

    def translate_comic(self) -> None:
        for input_filename, output_filename in zip(self.input_paths, self.output_paths):
            self.for_test_translate_single_page(input_filename, output_filename)

    def for_test_translate_single_page(
        self, input_filename: str, output_filename: str
    ) -> None:
        """
        This carry out the translat process, but save checkpoints in between.
        """
        img_to_translate = imgutils.load(input_filename, imgutils.IMAGE)
        # segment image: with and without text (see output and text directories)
        img_without_text, img_with_text = segment_image(img_to_translate)

        # save segmented images
        imgutils.save(output_filename.replace("outputs", "segmented"), img_without_text)
        imgutils.save(output_filename.replace("outputs", "text"), img_with_text)

        img_without_text = Image.fromarray(img_without_text).convert("RGB")

        i = 0
        rects = detect_text(img_with_text)
        for (x, y, width, height), cropped in rects:
            string = get_text(cropped)
            string = self.clean_text(string)
            string = translate(
                string, source_lang="english", target_lang="spanish"
            )

            drawed_text = Image.fromarray(cropped).convert("RGB")
            drawed_text.save(output_filename.replace("outputs", "detected").replace(".png", f"_{i}.png"))

            target_image = img_without_text.crop((x, y, x + width, y + height))
            if self.is_valid_text(string):
                drawed_text = get_drawed_text((width, height), string, self.font)

            drawed_text.save(output_filename.replace("outputs", "results").replace(".png", f"_{i}.png"))

            target_image = ImageChops.multiply(drawed_text, target_image)
            img_without_text.paste(target_image, (x, y))

            i += 1

        img_without_text.save(output_filename)

    def clean_text(self, text: str) -> str:
        """TODO: Implement a cleaning methodology"""
        return text

    def is_valid_text(self, text: str) -> bool:
        """
        TODO: Improve the text validation methodology with natural langeages
        processing techniques
        """
        text = text.strip()
        return len(text) > 3

    def translate_single_page(
        self, input_filename: str, output_filename: str
    ) -> None:
        img_to_translate = imgutils.load(input_filename, imgutils.IMAGE)
        # segment image: with and without text (see output and text directories)
        img_without_text, img_with_text = segment_image(img_to_translate)
        img_without_text = Image.fromarray(img_without_text).convert("RGB")

        rects = detect_text(img_with_text)
        for (x, y, width, height), cropped in rects:
            string = get_text(cropped)
            string = self.clean_text(string)
            string = translate(
                string, source_lang="english", target_lang="spanish"
            )

            drawed_text = Image.fromarray(cropped).convert("RGB")
            target_image = img_without_text.crop((x, y, x + width, y + height))
            if self.is_valid_text(string):
                drawed_text = get_drawed_text((width, height), string, self.font)

            target_image = ImageChops.multiply(drawed_text, target_image)
            img_without_text.paste(target_image, (x, y))

        img_without_text.save(output_filename)
