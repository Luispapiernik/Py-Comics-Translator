import os
from argparse import ArgumentParser
from os import path

import manga_babel.utils.image_utils as imgutils
from manga_babel.segmenter_model import segment_image


def execute(args):
    paths = [args.one_image]
    if args.one_image == "":
        paths = [
            filename for filename in os.listdir(args.input_folder)
            if imgutils.is_img_file(path.join(args.input_folder, filename))
        ]

    for imagename in paths:
        imagepath = path.join(args.input_folder, imagename)
        outputpath = path.join(args.output_folder, imagename)
        textpath = path.join(args.text_folder, imagename)

        image = imgutils.load(imagepath, imgutils.IMAGE)
        output, text = segment_image(image)

        imgutils.save(outputpath, output)
        imgutils.save(textpath, text)


def main():
    parser = ArgumentParser()

    parser.add_argument("-oi", "--one-image", default="")
    parser.add_argument("-i", "--input-folder", default="./images/inputs")
    parser.add_argument("-o", "--output-folder", default="./images/outputs")
    parser.add_argument("-t", "--text-folder", default="./images/text")

    args = parser.parse_args()

    execute(args)

if __name__ == "__main__":
    main()
