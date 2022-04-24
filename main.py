import argparse
from argparse import ArgumentParser

from comic_babel.comic_translator import ComicTranslator


def execute(args: argparse.Namespace) -> None:
    comic_translator = ComicTranslator(
        input_folder=args.input_folder,
        output_folder=args.output_folder,
        filename_regex=args.filename_regex,
        font_path=args.font_path,
    )
    comic_translator.translate_comic()


def main() -> None:
    parser = ArgumentParser()

    # agregar soporte para todo tipo de imagenes: PNG
    # TODO: add options for differents fonts, differents OCR's, differents
    # translators, differents image segmentators, differents contours detectors ...
    parser.add_argument("-f", "--filename-regex", default=r"\w+_\d+\.(?:jpg|png)")
    parser.add_argument("-i", "--input-folder", default="./images/inputs")
    parser.add_argument("-o", "--output-folder", default="./images/outputs")

    parser.add_argument(
        "-fp", "--font-path", default="./resources/fonts/Comic_Neue/ComicNeue-Bold.ttf"
    )

    args = parser.parse_args()

    execute(args)


if __name__ == "__main__":
    main()
