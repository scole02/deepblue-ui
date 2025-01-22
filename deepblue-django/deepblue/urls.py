"""
URL configuration for deepblue project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from deepblue_maps import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('map/', views.MapView.as_view(), name='deepblue_map'),
    path('api/get-path-points/', views.get_path_points, name='get_path_points'),
    path('api/get-fake-detections/', views.get_fake_detections, name='get_fake_detections'),
    path('api/detections/<int:detection_id>/', views.get_detection_details, name='get_detection_details'),
    path('api/detections/<int:detection_id>/review/', views.update_detection_review, name='update_detection_review'),
    path('api/all-detections/', views.get_all_detections, name='get_all_detections'),
    path('api/all-positive-detections/', views.get_all_positive_detections, name='get_all_positive_detections'),

]

# Add this to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
