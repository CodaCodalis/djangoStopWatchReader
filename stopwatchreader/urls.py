from django.urls import path
from .views import HomePageView, WebcamView, upload_image, upload_images, yolo

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("webcam/", WebcamView.as_view(), name="webcam"),
    path('upload_image/', upload_image, name='upload_image'),
    path('upload_images/', upload_images, name='upload_images'),
    path("yolo/", yolo, name="yolo"),
]
