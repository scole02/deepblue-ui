from django.shortcuts import render
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.gis.geos import Point
import json
from .utils.fake_data import generate_random_path

class MapView(View):
    template_name = 'deepblue_maps/map.html'

    def get(self, request):
        context = {
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
        }
        return render(request, self.template_name, context)

@require_http_methods(["POST"])
def get_path_points(request):
    try:
        # Parse the JSON data from request body
        data = json.loads(request.body)
        start_coord = data.get('start')
        end_coord = data.get('end')

        # Validate input
        if not start_coord or not end_coord:
            return JsonResponse({'error': 'Missing coordinates'}, status=400)

        # Extract lat/lng
        start_lat = float(start_coord['lat'])
        start_lng = float(start_coord['lng'])
        end_lat = float(end_coord['lat'])
        end_lng = float(end_coord['lng'])


        path_points = generate_random_path((start_lat, start_lng), (end_lat, end_lng))

        # Create path points
        # path_points = [{'lat': float(lat), 'lng': float(lng)} 
        #               for lat, lng in zip(lats, lngs)]

        return JsonResponse({
            'points': path_points,
            'total_points': len(path_points)
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
def get_fake_detections(request):
    try:
        # Parse the JSON data from request body
        data = json.loads(request.body)
        path = data.get('path', [])
        
        if not path:
            return JsonResponse({'error': 'No path provided'}, status=400)

        # Get or create a ModelParams instance for these detections
        model_params, created = ModelParams.objects.get_or_create(
            name='StarSeg',
            defaults={
                'classes': ['starfish'],
                'filepath': 'models/starseg_v1.pt'
            }
        )

        # Generate between 3 and 8 random detections
        num_detections = random.randint(3, 8)
        detection_ids = []

        for _ in range(num_detections):
            # Pick a random point along the path
            point_index = random.randint(0, len(path) - 1)
            point = path[point_index]
            
            # Add small random offset to make it look more natural
            lat_offset = random.uniform(-0.0001, 0.0001)
            lng_offset = random.uniform(-0.0001, 0.0001)
            
            # Create the detection
            detection = Detection.objects.create(
                model=model_params,
                location=Point(
                    float(point['lng']) + lng_offset,
                    float(point['lat']) + lat_offset
                ),
                likely_class='starfish',
                img='detections/starfish1.png',
                confidences={
                    'starfish': round(random.uniform(0.80, 0.99), 2)
                }
            )
            
            detection_ids.append(detection.id)

        return JsonResponse({
            'detection_ids': detection_ids,
            'total_detections': len(detection_ids)
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
