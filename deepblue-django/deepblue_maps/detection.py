import os
import json
from datetime import datetime
from ultralytics import YOLO
from django.conf import settings
from deepblue_maps.models import *

class DetectionHandler:
    def __init__(self, model_path="ckpts/yolo11n.pt", save_path="detections/"):
        self.model = YOLO(model_path)  
        self.save_path = os.path.join(settings.MEDIA_ROOT, save_path)

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def run_detection(self, video_path, confidence_threshold=0.5):
        try:
            video_path = os.path.join(settings.MEDIA_ROOT, video_path)
            results = self.model.predict(video_path, conf=confidence_threshold)
            detections = []
            time_stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_dir = os.path.join(self.save_path, f"detection_result_{time_stamp}/")
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                
            for idx, result in enumerate(results):
                for box in result.boxes:
                    conf = float(box.conf)
                    detection = {
                        "class": result.names[int(box.cls)],
                        "confidence": conf,
                        "bbox": [float(coord) for coord in box.xyxy[0].tolist()] 
                    }
                    detections.append(detection)
                save_path = os.path.join(save_dir, f"frame_{idx+1:04d}.jpg")
                result.save(save_path)


            result_file = os.path.join(self.save_path, f"detection_{time_stamp}.json")
            with open(result_file, "w") as f:
                json.dump(detections, f, indent=4)
                

            detection_entry = DetectionResult.objects.create(
                video_path=video_path,
                result_img_dir=save_dir,
                results_file=result_file,
                detections=detections
            )

            return {"status": "success", "detections": detections, "db_id": detection_entry.id}

        except Exception as e:
            return {"status": "error", "message": str(e)}