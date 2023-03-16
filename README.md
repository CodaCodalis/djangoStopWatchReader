# StopWatchReader

## Installation:

1. Install Python 3.7
2. Install PIP
3. Clone this repository: `git clone https://github.com/CodaCodalis/djangoStopWatchReader.git`
4. Go to project directory: `cd djangoStopWatchReader`
5. Install virtual environment: `python -m venv .venv`
6. Activate virtual environment: `.venv\Scripts\activate`
7. Install requirements: `pip install -r requirements.txt`
8. Download [yolov4.weights](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights) (or [here](https://drive.google.com/open?id=1cewMfusmPjYWbrnuJRuKhPMwRe_b9PaT)) and save it in the project folder in `static/resources/`

## Usage:

1. Activate virtual environment: `.venv\Scripts\activate` (if not already activated)
2. Run `python manage.py runserver`
3. Open `http://127.0.0.1:8000/` in your browser

## How it works:
1. WebcamReader: Reads the webcam, returns the processed selection and the recognized digits
2. UploadReader: Reads the uploaded image(s), returns some processed steps and the recognized digits
3. YOLOv4Reader: Reads the uploaded image(s), returns the image with marked recognized objects (in a future version possibly stopwatches)