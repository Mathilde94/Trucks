from django.db import models

class Truck(models.Model):
    """
    Truck model
    
    Applicant: the name of the truck
    Latitude: Latitude of the truck location
    Longitude: Longitude of the truck location
    Category: Category of food served
    """

    applicant = models.CharField(max_length=250)
    latitude = models.FloatField() 
    longitude = models.FloatField()
    category = models.CharField(max_length=250)
