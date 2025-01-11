from django.shortcuts import render
from django.conf import settings
from django.views import View


class MapView(View):
    template_name = 'deepblue_maps/map.html'

    def get(self, request):
        context = {
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
        }
        return render(request, self.template_name, context)
