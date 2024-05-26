# Stripe Color Detection Assignment

This project involves detecting the color of each block inside a stripe. The process consists of using contour detection to find all the squares in the stripe and then determining the color inside each detected contour.

## Table of Contents
1. [Introduction](#introduction)
2. [Contour Detection](#contour-detection)
3. [Color Detection](#color-detection)
4. [Django Integration](#django-integration)
5. [Conclusion](#conclusion)

## Introduction

In this project, we aim to accurately detect the color of blocks within a striped image. The main steps include:
- Detecting contours to identify block boundaries.
- Analyzing the colors within these detected contours.

## Contour Detection

To find all the squares in the stripe, we utilize contour detection. Contours are useful for shape analysis and object detection and recognition.

### Steps for Contour Detection

1. **Convert Image to Grayscale**:
    ```python
    import cv2

    image = cv2.imread('path_to_image')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ```

2. **Apply Edge Detection**:
    ```python
    edges = cv2.Canny(gray, threshold1=30, threshold2=100)
    ```

3. **Find Contours**:
    ```python
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ```

4. **Draw Contours** (optional for visualization):
    ```python
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
    ```

## Color Detection

After detecting the contours, we proceed to determine the color within each contour.

### Steps for Color Detection

1. **Loop through each contour**:
    ```python
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = image[y:y+h, x:x+w]
    ```

2. **Calculate the Mean Color**:
    ```python
    mean_color = cv2.mean(roi)[:3]  # BGR format
    ```

3. **Convert BGR to RGB**:
    ```python
    mean_color_rgb = (mean_color[2], mean_color[1], mean_color[0])
    ```

4. **Determine the Dominant Color** (optional):
    ```python
    from collections import Counter
    colors = roi.reshape(-1, roi.shape[-1])
    dominant_color = Counter(map(tuple, colors)).most_common(1)[0][0]
    ```

## Django Integration

To integrate this functionality into a Django website, follow these steps:

### Setting Up the Django Project

1. **Create a Django Project**:
    ```bash
    django-admin startproject stripe_color_detection
    cd stripe_color_detection
    ```

2. **Create an App**:
    ```bash
    python manage.py startapp color_detector
    ```

3. **Configure `settings.py`**:
    ```python
    INSTALLED_APPS = [
        ...
        'color_detector',
    ]
    ```

### Building the Views

1. **Create a View for Image Upload and Processing**:
    ```python
    # color_detector/views.py

    from django.shortcuts import render
    from django.core.files.storage import FileSystemStorage
    import cv2

    def upload_image(request):
        if request.method == 'POST' and request.FILES['image']:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)

            # Process the image
            img = cv2.imread(fs.path(filename))
            # (Insert contour and color detection code here)

            context = {
                'uploaded_file_url': uploaded_file_url,
                # Add any other context variables needed
            }
            return render(request, 'color_detector/result.html', context)
        return render(request, 'color_detector/upload.html')
    ```

2. **Create Templates**:
    - `upload.html`:
        ```html
        <!DOCTYPE html>
        <html>
        <body>
            <h2>Upload an Image</h2>
            <form method="POST" enctype="multipart/form-data">
                {% csrf_token %}
                <input type="file" name="image">
                <button type="submit">Upload</button>
            </form>
        </body>
        </html>
        ```
    - `result.html`:
        ```html
        <!DOCTYPE html>
        <html>
        <body>
            <h2>Uploaded Image</h2>
            <img src="{{ uploaded_file_url }}" alt="Uploaded Image">
            <!-- Display results here -->
        </body>
        </html>
        ```

3. **Configure URLs**:
    ```python
    # stripe_color_detection/urls.py

    from django.contrib import admin
    from django.urls import path
    from color_detector import views

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('upload/', views.upload_image, name='upload_image'),
    ]
    ```

## Conclusion

This document outlines the steps for detecting the color of blocks in a stripe using contour detection and integrating this functionality into a Django website. The combination of OpenCV for image processing and Django for web development provides a robust solution for this task.
