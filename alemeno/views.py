from django.shortcuts import render
from django.conf import settings
from .forms import ImageUploadForm
from PIL import Image
import os

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()  # Save the form to get the uploaded image instance
            image_path = os.path.join(settings.MEDIA_ROOT, str(image_instance.image))
            rgb_values = process_image(image_path)  # Process the uploaded image
            image_url = settings.MEDIA_URL + str(image_instance.image)  # Construct the URL of the uploaded image
            response = {"form": form, "image_url": image_url, "rgb_values": rgb_values}
            return render(request, 'display_image.html', response)
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

def process_image(image_path):
    try:
        with Image.open(image_path) as img:
            # Ensure image is in RGB mode
            rgb_image = img.convert('RGB')
            pixels = list(rgb_image.getdata())
            return pixels[:10]  # Returning first 10 RGB values as an example
    except Exception as e:
        return f"An error occurred: {str(e)}"
