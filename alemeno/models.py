from django.db import models

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='images/')  
    
    class Meta:
        app_label = 'alemeno'