from django.views.generic import TemplateView
from django.http import JsonResponse
from PIL import Image


class HomePageView(TemplateView):
    template_name = "home.html"


class WebcamView(TemplateView):
    template_name = "webcam.html"


class PhotoView(TemplateView):
    template_name = "photo.html"


class YoloView(TemplateView):
    template_name = "yolov4.html"


def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        # save image to file system
        image = Image.open(image)
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save('static/resources/image.jpg')
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
