# StopWatchReader

## Installation:

1. Install Python 3.7
2. Install PIP
3. Clone this repository: `git clone https://github.com/CodaCodalis/djangoStopWatchReader.git`
4. Go to project directory: `cd djangoStopWatchReader`
5. Install virtual environment: `python -m venv .venv`
6. Activate virtual environment: `source .venv\bin\activate` (might be different on Windows)
7. Install requirements: `pip install -r requirements.txt`
8. Download [yolov4.weights](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights) (or [here](https://drive.google.com/open?id=1cewMfusmPjYWbrnuJRuKhPMwRe_b9PaT)) and save it in the project folder in `static/resources/`

## Usage:

1. Activate virtual environment: `source .venv\bin\activate` (if not already activated)
2. Run `python manage.py runserver`
3. Open `http://127.0.0.1:8000/` in your browser

## How it works:
1. WebcamReader: 
    - reads the webcam
    - crops the image to the region of interest (ROI)
    - processes the selection to prepare it for optical character recognition (OCR)
    - returns the processed selection
    - returns the digits recognized by OCR
2. UploadReader: 
    - reads the uploaded image(s)
    - tries to find a stopwatch in the image using a mask image
    - rotates the input image if necessary
    - tries to segment the display
    - crops the image to the ROI
    - processes the selection to prepare it for OCR
    - returns the original image and some processed images for debugging
    - returns the recognized digits
3. YOLOv4Reader:
    - reads the uploaded image(s)
    - returns the image with marked recognized objects 
    - in a future version possibly recognizes stopwatches