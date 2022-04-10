import os
import re

import cv2

import comic_babel.utils.image_utils as imgutils
from comic_babel.segmenter_model import segment_image
from comic_babel.text_detector import detect_text
from comic_babel.text_extractor import get_text


class ComicTranslator:
    def __init__(self, *, input_folder, output_folder, filename_regex):
        # get valid paths
        valid_paths = [
            filename
            for filename in os.listdir(input_folder)
            if (
                re.fullmatch(filename_regex, filename)
                and imgutils.is_img_file(os.path.join(input_folder, filename))
            )
        ]

        self.input_paths = [
            os.path.join(input_folder, filename)
            for filename in valid_paths
        ]

        self.output_paths = [
            os.path.join(output_folder, filename)
            for filename in valid_paths
        ]

    def translate_comic(self):
        # TODO: fix problems with paralelization
        # import multiprocessing as mp
        # pool = mp.Pool(mp.cpu_count())
        # pool.imap_unordered(
        #     self.translate_single_page, zip(self.input_paths, self.output_paths)
        # )
        # pool.close()
        # pool.join()

        for input_filename, output_filename in zip(self.input_paths, self.output_paths):
            self.translate_single_page(input_filename, output_filename)

    def translate_single_page(self, input_filename, output_filename):
        image = imgutils.load(input_filename, imgutils.IMAGE)
        without_text, text = segment_image(image)

        imgutils.save(output_filename, without_text)
        imgutils.save(output_filename.replace("outputs", "text"), text)

        rects = detect_text(text)
        print("=" * 100)
        for (x, y, width, height), cropped in rects:
            string = get_text(cropped)
            if string.strip() != "":
                print(string)
                print("-" * 100)

            offset = 0
            left_top = (x - offset, y - offset)
            bottom_right = (x + width + offset, y + height + offset)
            cv2.rectangle(
                text,
                left_top,
                bottom_right,
                color=(0, 0, 0),
                thickness=1
            )

        imgutils.save(output_filename.replace("outputs", "detected"), text)
