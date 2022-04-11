import os
import re

import cv2
from PIL import Image

import comic_babel.utils.image_utils as imgutils
from comic_babel.drawer import get_drawed_text
from comic_babel.segmenter_model import segment_image
from comic_babel.text_detector import detect_text
from comic_babel.text_extractor import get_text


class ComicTranslator:
    """
    Class with all translating process of the comic specified.

    TODO: remember recursiveness reading the images to be translated
        file_list = [file for sub_dir in os.walk(self.path) for file in glob.glob(os.path.join(sub_dir[0], '*.root'))]

    Parameters
    ------------
    input_folder: str
        dummy info
    ouput_folder: str
    filename_regex: str
    """

    def __init__(
        self, *, input_folder: str, output_folder: str, filename_regex: str
    ) -> None:
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

    def translate_comic(self):
        for input_filename, output_filename in zip(self.input_paths, self.output_paths):
            self.translate_single_page(input_filename, output_filename)

    def for_test_translate_single_page(self, input_filename, output_filename):
        """
        This carry out the translat process, but save checkpoints in between.
        """
        img_to_translate = imgutils.load(input_filename, imgutils.IMAGE)
        # segment image: with and without text (see output and text directories)
        img_without_text, img_with_text = segment_image(img_to_translate)

        # save segmented images
        imgutils.save(output_filename, img_without_text)
        imgutils.save(output_filename.replace("outputs", "text"), img_with_text)

        # obtain subimages that have the texts in the img_to_translate
        rects = detect_text(img_with_text)
        print("=" * 100)
        i = 0
        # go over the subimages obtain text, shift a little, and put in
        #  the image again.
        for (x, y, width, height), cropped in rects:
            string = get_text(cropped)
            if string.strip() != "":
                print(string)
                print("-" * 100)

            offset = 0
            left_top = (x - offset, y - offset)
            bottom_right = (x + width + offset, y + height + offset)
            cv2.rectangle(
                img_with_text,
                left_top,
                bottom_right,
                color=(0, 0, 0),
                thickness=1
            )

            imgutils.save(
                output_filename.replace("outputs", "cropped").replace(".png", f"_{i}.png"),
                cropped
            )
            i += 1

        imgutils.save(output_filename.replace("outputs", "detected"), img_with_text)

    def clean_text(self, text: str) -> str:
        """TODO: Implement a cleaning methodology"""
        return text

    def is_valid_text(self, text: str) -> bool:
        """TODO: Improve the text validation methodology"""
        text = text.strip()
        return len(text) > 2

    def translate_single_page(self, input_filename, output_filename):
        img_to_translate = imgutils.load(input_filename, imgutils.IMAGE)
        # segment image: with and without text (see output and text directories)
        img_without_text, img_with_text = segment_image(img_to_translate)
        img_without_text = Image.fromarray(img_without_text).convert("RGB")

        rects = detect_text(img_with_text)
        for (x, y, width, height), cropped in rects:
            string = get_text(cropped)
            string = self.clean_text(string)

            drawed_text = Image.fromarray(cropped)
            if self.is_valid_text(string):
                drawed_text = get_drawed_text((width, height), string)

            img_without_text.paste(drawed_text, (x, y))

        img_without_text.save(output_filename)
