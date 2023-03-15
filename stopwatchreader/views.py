import base64
from io import BytesIO

from django.views.generic import TemplateView
from django.http import JsonResponse
from PIL import Image
from .utils import prepare, analyze


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
        # image = Image.open(image)
        # if image.mode == 'RGBA':
        #     image = image.convert('RGB')

        cropped_image = prepare(image)
        text = analyze(cropped_image)
        # image.save('static/resources/image.jpg')
        # print(text)

        cropped_image = Image.fromarray(cropped_image)
        # cropped_image.save('static/resources/image.jpg')
        # decode image to base64
        cropped_image_bytes = BytesIO()
        cropped_image.save(cropped_image_bytes, format='JPEG')
        cropped_image_base64 = base64.b64encode(cropped_image_bytes.getvalue()).decode('utf-8')

        return JsonResponse({'success': True,
                             'result': text,
                             'image': cropped_image_base64
                             })
    else:
        return JsonResponse({'success': False})
