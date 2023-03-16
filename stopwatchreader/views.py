import base64
from io import BytesIO

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from PIL import Image
from .utils import prepare, analyze, process_image
from .forms import ImageUploadForm


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
        cropped_image = prepare(image)
        text = analyze(cropped_image)

        # decode image to base64
        cropped_image = Image.fromarray(cropped_image)
        cropped_image_bytes = BytesIO()
        cropped_image.save(cropped_image_bytes, format='JPEG')
        cropped_image_base64 = base64.b64encode(cropped_image_bytes.getvalue()).decode('utf-8')

        return JsonResponse({'success': True,
                             'result': text,
                             'image': cropped_image_base64
                             })
    else:
        return JsonResponse({'success': False})


def upload_images(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            images = form.cleaned_data['images']
            results = []
            for image in images:
                img1, img2, img3 = process_image(image)
                # img1_bytes = BytesIO
                # img1.save(img1_bytes, format='JPEG')
                # img1_base64 = base64.b64encode(img1_bytes.getvalue()).decode('utf-8')
                results.append({
                    'step1': img1,
                    # 'step2': img2,
                    # 'step3': img3,
                })
            return JsonResponse({'results': results})
    else:
        form = ImageUploadForm()
    return render(request, 'upload_images.html', {'form': form})


def yolo(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_name = file.name
        file_size = file.size

        # return image with recognized objects

        return HttpResponse('File uploaded successfully: ' + file_name + ' (' + str(file_size) + ' bytes)')
    return render(request, 'yolov4.html')
