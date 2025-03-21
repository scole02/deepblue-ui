from django.contrib import admin
from .models import ModelParams, Detection, Transect, VideoRecording, DetectionResult

admin.site.register(ModelParams)
admin.site.register(Detection)
admin.site.register(Transect)
admin.site.register(VideoRecording)
admin.site.register(DetectionResult)

