from django.conf.urls import patterns, url, include
from rest_framework import routers, serializers, viewsets

from truck.views import TruckViewSet

# Router of the rest framework for the truck API
router = routers.DefaultRouter()
router.register(r'trucks', TruckViewSet)

urlpatterns = patterns('',
                       url(r'', include(router.urls)),
)

