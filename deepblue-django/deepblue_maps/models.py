from django.db import models
from django.contrib.gis.db import models as gis_models

class ModelParams(models.Model):
    filepath = models.FileField(max_length=255, upload_to='models/')
    name = models.CharField(max_length=100)
    classes = models.JSONField()  # Stores a list of classesE

    def __str__(self):
        return self.name

class Transect(models.Model):
    start_point = gis_models.PointField()
    end_point = gis_models.PointField()
    time_started = models.DateTimeField()
    time_ended = models.DateTimeField(null=True, blank=True)


class Detection(models.Model):
    model = models.ForeignKey(ModelParams, on_delete=models.CASCADE, related_name="detections")
    transect = models.ForeignKey(Transect, null=True, blank=True, on_delete=models.CASCADE, related_name="detections")  # New foreign key
    location = gis_models.PointField()  # Combines lat and long
    likelyClass = models.CharField(max_length=50)  # Changed from likely_class
    img = models.ImageField(upload_to='detections/')  # Stores the image file
    time = models.DateTimeField(auto_now_add=True)  # Automatically adds the timestamp
    confidences = models.JSONField()  # Stores a list of confidence scores with class names as keys
    isFalsePositive = models.BooleanField(null=True, default=None) # variable that is None by default, and True or False based on user input
    depth = models.FloatField(null=True, blank=True)

    def __str__(self):
        
        return f"Detection: {self.likelyClass} at {self.time}"