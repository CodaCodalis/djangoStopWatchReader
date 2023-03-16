import cv2
import numpy as np
from PIL import Image
import pytesseract


def prepare(image):
    # convert to RGB if necessary
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


def prepare_upload(image):
    # convert to RGB if necessary
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    img = np.array(image)
    # img = cv2.imread(image)

    # convert to grey-scale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # some gaussian blur
    img = cv2.GaussianBlur(img, (1, 1), 0)
    # threshold filter
    img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)[1]
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
    image = np.array(image)
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    # step1
    # step1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = cv2.imread('static/resources/mask_stopwatch_display_color.jpg')
    step1 = find_stopwatch(mask, image)

    # step2
    # step2 = cv2.GaussianBlur(step1, (1, 1), 0)
    mask = cv2.imread('static/resources/mask_stopwatch_display_color_near.jpg')
    step2 = find_display(mask, step1)

    # step3
    # step3 = cv2.threshold(step2, 160, 255, cv2.THRESH_BINARY)[1]
    step3 = prepare_upload(Image.fromarray(step2))
    text = analyze(step3)

    step1 = Image.fromarray(step1)
    step2 = Image.fromarray(step2)
    step3 = Image.fromarray(step3)

    # pack all steps into a list
    step_list = [step1, step2, step3]
    return step_list, text


def find_stopwatch(mask, img):
    # Convert the mask to grayscale
    gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to the grayscale mask
    _, binary_mask = cv2.threshold(gray_mask, 127, 255, cv2.THRESH_BINARY)

    # Find the contour of the triangle in the binary mask
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    stopwatch_contour = max(contours, key=cv2.contourArea)

    # Extract the bounding rectangle of the triangle
    x, y, w, h = cv2.boundingRect(stopwatch_contour)

    # Crop the binary mask to the dimensions of the bounding rectangle
    cropped_mask = binary_mask[y:y + h, x:x + w].astype(np.uint8)

    # Convert the cropped mask to grayscale
    cropped_mask = cv2.cvtColor(cropped_mask, cv2.COLOR_GRAY2BGR)

    # Perform template matching to locate the triangle in the original image
    result = cv2.matchTemplate(img, cropped_mask, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)

    # Extract the coordinates of the top-left corner of the template
    top_left = max_loc

    # Create a rectangle using the template dimensions
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 2)

    # Crop the original image to the dimensions of the template
    cropped_img = img[top_left[1]:top_left[1] + h, top_left[0]:top_left[0] + w]

    # return the cropped image
    return cropped_img


def find_display(mask, img):
    # Convert the mask to grayscale
    gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to the grayscale mask
    _, binary_mask = cv2.threshold(gray_mask, 127, 255, cv2.THRESH_BINARY)

    # Find the contour of the triangle in the binary mask
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    stopwatch_contour = max(contours, key=cv2.contourArea)

    # Extract the bounding rectangle of the triangle
    x, y, w, h = cv2.boundingRect(stopwatch_contour)

    # Crop the binary mask to the dimensions of the bounding rectangle
    cropped_mask = binary_mask[y:y + h, x:x + w].astype(np.uint8)

    # Convert the cropped mask to grayscale
    cropped_mask = cv2.cvtColor(cropped_mask, cv2.COLOR_GRAY2BGR)

    # Perform template matching to locate the triangle in the original image
    result = cv2.matchTemplate(img, cropped_mask, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)

    # Extract the coordinates of the top-left corner of the template
    top_left = max_loc

    # Create a rectangle using the template dimensions
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 2)

    # Crop the original image to the dimensions of the template
    cropped_img = img[top_left[1]:top_left[1] + h, top_left[0]:top_left[0] + w]

    # return the cropped image
    return cropped_img


def yolo_recognize(img):
    img = np.array(img)
    # Load the YOLOv4 network
    net = cv2.dnn.readNet("static/resources/yolov4.weights", "static/resources/yolov4.cfg")

    # Get the names of the output layers
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # Convert image
    img = cv2.convertScaleAbs(img)

    # Run the YOLOv4 network on the image
    blob = cv2.dnn.blobFromImage(img, scalefactor=1 / 255.0, size=(416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Get the dimensions of the input image
    height, width, channels = img.shape

    # Process the YOLOv4 output
    conf_threshold = 0.5
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                # Convert the relative coordinates to absolute coordinates
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # Apply non-maximum suppression to remove overlapping bounding boxes
    nms_threshold = 0.4
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    classes = []
    with open("static/resources/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # Draw the bounding boxes and class labels on the image
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(class_ids), 3))
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            conf = str(confidences[i])
            label = str(classes[class_ids[i]]) + " " + conf[0:4]
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y - 5), font, 2, color, 2)

    img = Image.fromarray(img)
    return img
