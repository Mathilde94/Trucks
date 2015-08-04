#!/usr/bin/env python

##
# generate.py
# This file is to create/generate the database coming
# from https://data.sfgov.org/resource/rqzj-sfat.json
##

import os
import sys
import django
import traceback
import json
from datetime import datetime
from django.utils import timezone
import urllib2, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../truck"))

# Main variables
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Trucks.settings")
DATA_URL = "https://data.sfgov.org/resource/rqzj-sfat.json"

from Trucks import settings
from truck.models import Truck

def delete_entities():
    """ 
    This call is to delete and then clean the DB 
    """

    Truck.objects.all().delete()

def usage():
    """
    Show the usage of this file
    """

    sys.exit("Usage: python Database/generate.py show|rebuild [database]")

def fetch_all_trucks(url):
    """
    Fetch all the truck from the url 
    """

    try:
        f = urllib2.urlopen(url)
        data = json.loads(f.read())    
    except Exception as e:
        print "We encountered an error fetching the trucks:"
        print e
        sys.exit(1)

    trucks = []

    # Noticed there are a few duplicates entries that has the same latlong
    # but same names, so we can jsut remove duplicates:
    latlong = {}
    for truck in data:

        if truck.get('latitude', False) and truck.get('longitude', False):
            latitude, longitude = float(truck['latitude']), float(truck['longitude'])
            name = UpperFirst(str(truck['applicant']))
            category = UpperFirst(str(truck.get('fooditems', '').split(":")[0]))

            truck_data = {
                'latitude': latitude, 
                'longitude': longitude,
                'name': name,
                'category': category
            }

            if (latitude, longitude) not in latlong.keys():
                latlong[(latitude, longitude)] = truck_data
                trucks.append(truck_data)

    return trucks

def UpperFirst(string_name):
    """
    Lower all the cases of the string except the first one
    """

    if len(string_name) == 0:
        return ""

    if len(string_name) == 1:
        return string_name.upper()

    string_name = string_name.lower()
    string_name = string_name[0].upper() + string_name[1:]

    return string_name


def rebuild_database():
    """
    Let's build the database from scratch with the DB from 
    https://data.sfgov.org/resource/rqzj-sfat.json
    """

    trucks = fetch_all_trucks(DATA_URL)

    for truck in trucks:

        truck = Truck(applicant = truck['name'], 
                      latitude = truck['latitude'], 
                      longitude = truck['longitude'],
                      category = truck['category']
        )
        truck.save()

def show_database():
    """
    Show the database
    """

    trucks = Truck.objects.all()

    for truck in trucks:
        print truck.applicant, '\t', truck.category, \
            '\t', truck.latitude, truck.longitude


if __name__ == '__main__':

    if len(sys.argv) < 2:
        usage()

    django.setup()

    if sys.argv[1] == "show":
        print "Show the database ..."
        show_database()

    elif sys.argv[1] == "rebuild":
        print "Rebuilding the database ..."
        try:
            delete_entities()
            rebuild_database()
        except Exception as e:
            print
            print "We encountered an error while rebuilding the database"
            print e
            print traceback.format_exc(e)
    else:
        usage()

