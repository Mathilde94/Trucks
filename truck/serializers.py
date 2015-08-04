from rest_framework import serializers
from rest_framework import routers, serializers, viewsets, filters

from truck.models import Truck

# Truck Serializer defining the API representation.
class TruckSerializer(serializers.ModelSerializer):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('category')

    class Meta:
        model = Truck
        fields = ('applicant', 'latitude', 'longitude', 'category', 'id')

