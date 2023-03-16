import os

import cv2
import numpy as np
from PIL import Image
import pytesseract

from django_project import settings


def prepare(image):
    image = Image.open(image)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    # crop image to selected area
    left = (640 - 280) / 2
    top = (480 - 80) / 2
    right = left + 280
    bottom = top + 80
    cropped_image = image.crop((left, top, right, bottom))

    img = np.array(cropped_image)
    # img = cv2.imread(image)

    # convert to grey-scale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # some gaussian blur
    img = cv2.GaussianBlur(img, (1, 1), 0)
    # threshold filter
    img = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)[1]
    # invert if more black than white pixels
    number_of_white_pix = np.sum(img == 255)
    number_of_black_pix = np.sum(img == 0)
    if number_of_black_pix > number_of_white_pix:
        img = cv2.bitwise_not(img)

    return img


def analyze(image):
    # define custom config
    custom_config = r'--psm 7 --oem 3 --tessdata-dir "tessdata" -c tessedit_char_whitelist=".:0123456789 "'
    text = pytesseract.image_to_string(image, lang='7seg', config=custom_config)

    # use if other than 7seg font
    # text = pytesseract.image_to_string(img, lang='osd', config=custom_config)

    return text


def process_image(image):
    # perform processing steps on the image and return the paths of the processed images
    # you can use Pillow library for image processing
    # for example, you can resize the image to 200x200, apply a filter and convert it to grayscale
    img1 = image
    img2 = image
    img3 = image
    # ... do processing ...
    return img1, img2, img3
