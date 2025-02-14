from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils import timezone

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
    


class VideoRecording(models.Model):
    # video_file = models.FileField(upload_to='videos/')
    video_path = models.CharField(max_length=255,null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"VideoRecording {self.id} - {self.recorded_at}"
    
    

class DetectionResult(models.Model):
    video_path = models.CharField(max_length=500, help_text="video file path")
    results_file = models.CharField(max_length=500, help_text="detection results - json file path")
    result_img_dir = models.CharField(max_length=500, help_text="directory containing result images")
    detections = models.JSONField(default=list, help_text="list of detections")
    confidence_threshold = models.FloatField(default=0.5, help_text="confidence threshold")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DetectionResult {self.id} - {self.result_img_dir}"

