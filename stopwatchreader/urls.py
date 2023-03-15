from django.urls import path
from .views import HomePageView, WebcamView, PhotoView, YoloView, upload_image

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("webcam/", WebcamView.as_view(), name="webcam"),
    path('upload_image/', upload_image, name='upload_image'),
    path("photo/", PhotoView.as_view(), name="photo"),
    path("yolov4/", YoloView.as_view(), name="yolov4"),
]
