from argparse import ArgumentParser
from os import listdir, path

import cv2

import core
import imgio as io
from utils.imutils import is_img_file


def execute(args):
    paths = [args.one_image]
    if args.one_image == "":
        paths = [
            filename for filename in listdir(args.input_folder)
            if is_img_file(path.join(args.input_folder, filename))
        ]

    for imagename in paths:
        imagepath = path.join(args.input_folder, imagename)
        outputpath = path.join(args.output_folder, imagename)
        textpath = path.join(args.text_folder, imagename)

        image = io.load(imagepath, io.IMAGE)
        mask = core.segmap(image)

        output = core.inpainted(image, mask)
        text = cv2.bitwise_and(image, mask)
        text[mask == 0] = 255

        io.save(outputpath, output)
        io.save(textpath, text)


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
