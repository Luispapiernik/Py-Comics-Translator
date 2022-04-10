import cv2


# based on https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
def detect_text(image):
    # Convert the image to gray scale
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))

    # transformed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, rect_kernel)
    # Applying dilation on the threshold image
    transformed = cv2.dilate(thresh, rect_kernel, iterations=1)

    # Finding contours. The hierarchy
    # (https://docs.opencv.org/3.4/d9/d8b/tutorial_py_contours_hierarchy.html)
    # could be used to ignore some countous
    contours, hierarchy = cv2.findContours(
        transformed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    offset = 0
    result = []
    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, width, height = cv2.boundingRect(cnt)
        left_top = (x - offset, y - offset)
        bottom_right = (x + width + offset, y + height + offset)

        # TODO: this must be parametrized
        if width > 20 and height > 20:
            # Drawing a rectangle on copied image
            cv2.rectangle(
                image,
                left_top,
                bottom_right,
                color=(0, 0, 0),
                thickness=1
            )

        # Cropping the text block for giving input to OCR
        cropped = image[left_top[1]:bottom_right[1], left_top[0]:bottom_right[0]]
        result.append(((x, y, width, height), cropped))

    return result
