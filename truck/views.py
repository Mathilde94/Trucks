# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.http import Http404

# Rest Framework
from rest_framework import generics, filters, viewsets

# From truck
from truck.models import Truck
from truck.serializers import TruckSerializer 

# Import mathematic library
import math

DEFAULT_RADIUS = 2 #mile
EARTH_RADIUS = 6371000 # in m
ONE_MILE_IN_KM = 1.609344


class Point(object):

    def __init__(self, latitude, longitude):

        """
        Initialize a point with its coordinates
        """

        self.latitude = latitude
        self.longitude = longitude


    def compute_distance_square(self, truck):
        
        """
        Computes the distance square of a truck to this point
        based on latitudes and longitudes of those 2 points
        
        Based on this article: http://www.movable-type.co.uk/scripts/latlong.html
        
        :return: Their distance to each other in km
        """

        dlon = math.radians(self.longitude - truck.longitude)
        dlat = math.radians(self.latitude - truck.latitude)
        
        a = math.sin(dlat/2)**2
        b = math.cos(math.radians(self.latitude))
        b *= math.cos(math.radians(truck.latitude)) 
        b *= math.sin(dlon/2)**2 
        a+= b
        
        c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) ) 

        return EARTH_RADIUS * c / 1000

    def is_truck_close(self, truck, radius):

        """
        Function defining if a truck is in the radius zone of 
        this point
        :return: True if yes, False if not
        """

        distance_truck_point = self.compute_distance_square(truck)
        return distance_truck_point < radius * ONE_MILE_IN_KM

# ViewSets define the view behavior.
class TruckViewSet(viewsets.ModelViewSet):

    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    
    def get_object(self):
        """
        Get the truck item with the pk indicated in the URL
        """
        id = self.kwargs.get('pk', 1)
        truck = None
        try: 
            truck = Truck.objects.get(id=id)
        except ObjectDoesNotExist as e:
            raise Http404

        return truck
        
    def get_queryset(self):
        """
        Overwriting the get query set based on parameters of 
        the request
        """

        # Get the filters 
        queryset = Truck.objects.all()
        fields = ('latitude', 'longitude', 'category', 'radius')
        filters = dict((field, self.request.query_params.get(field, None)) 
                       for field in fields)


        # Filtering by category
        category = filters['category']

        if category is not None:
            queryset = queryset.filter(category__startswith=category)

        # Filtering by distance defined with a point and a radius
        latitude, longitude = filters['latitude'], filters['longitude']
        if latitude is not None and longitude is not None:
            radius = filters['radius']
            queryset = self.update_with_distance(queryset, 
                                                 radius, 
                                                 latitude, longitude)

        return queryset


    def update_with_distance(self, queryset, radius, latitude, longitude):
        """
        Update a set of trucks with the ones that are close in radius distance
        of the point defined by latitude/longitude

        :return: Queryset updated
        """

        if radius is not None:
            radius = float(radius)
        else:
            radius = DEFAULT_RADIUS

        point = Point(float(latitude), float(longitude))

        return filter(lambda truck: point.is_truck_close(truck, radius),
                              queryset)
