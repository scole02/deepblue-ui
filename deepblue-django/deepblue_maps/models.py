from django.db import models
from django.contrib.gis.db import models as gis_models

class ModelParams(models.Model):
    filepath = models.FileField(max_length=255, upload_to='models/')
    name = models.CharField(max_length=100)
    classes = models.JSONField()  # Stores a list of classesE

    def __str__(self):
        return self.name

class Detection(models.Model):
    model = models.ForeignKey(ModelParams, on_delete=models.CASCADE, related_name="detections")
    location = gis_models.PointField()  # Combines lat and long
    likely_class = models.CharField(max_length=50)
    img = models.ImageField(upload_to='detections/')  # Stores the image file
    time = models.DateTimeField(auto_now_add=True)  # Automatically adds the timestamp
    confidences = models.JSONField()  # Stores a list of confidence scores with class names as keys

    def __str__(self):
        return f"Detection: {self.likely_class} at {self.time}"