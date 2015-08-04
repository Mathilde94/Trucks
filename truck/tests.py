"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

"""
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status

from collections import OrderedDict

URL_ROOT='/api/trucks/'

class BasicTruckOperations(APITestCase):
    """
    APITestCase to test adding, getting and deleting operations
    """

    def test_add_truck(self):
        """
        This test function will: 
        - Add a first truck 
        - Get that truck
        - Update and check the new value
        - Filter per category
        - Remove that truck
        """

        # ------------------------------------------------------------
        # Let's create a new truck:
        data = {
            'applicant': "Truck 1",
            'latitude': 37.7901490737255, 
            'longitude': -122.398658184604,
            'category': "Cupcakes"
        }
        id = 1
        response = self.client.post(URL_ROOT, data, format='json')
        data.update({'id': id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)


        # ------------------------------------------------------------
        # Let s get the list of items:
        response_all = self.client.get(URL_ROOT, format='json')
        expected_output = [OrderedDict([
            ('applicant', u'Truck 1'), 
            ('latitude', 37.7901490737255), 
            ('longitude', -122.398658184604), 
            ('category', u'Cupcakes'), 
            ('id', 1)
        ])]
        self.assertEqual(response_all.status_code, status.HTTP_200_OK)
        self.assertEqual(response_all.data, expected_output)


        # ------------------------------------------------------------
        # Let's get now the item 
        url = "%s%s/" % (URL_ROOT, id) 
        response_item = self.client.get(url, format='json')
        self.assertEqual(response_item.status_code, status.HTTP_200_OK)
        self.assertEqual(response_item.data, data)


        # ------------------------------------------------------------
        # Let's now update the item 
        url = "%s%s/" % (URL_ROOT, id) 
        data.update({'category': 'Desserts'})
        response_item = self.client.put(url, data, format='json')
        self.assertEqual(response_item.status_code, status.HTTP_200_OK)
        self.assertEqual(response_item.data, data)


        # ------------------------------------------------------------
        # Let's get now the item 
        url = "%s%s/" % (URL_ROOT, id) 
        response_item = self.client.get(url, format='json')
        self.assertEqual(response_item.status_code, status.HTTP_200_OK)
        self.assertEqual(response_item.data, data)

        # ------------------------------------------------------------
        # Let's get now the item 
        filter_category="?category=Desserts"
        url = "%s%s" % (URL_ROOT, filter_category)
        response_filter = self.client.get(url, format='json')
        expected_output = [OrderedDict([
            ('applicant', u'Truck 1'), 
            ('latitude', 37.7901490737255), 
            ('longitude', -122.398658184604), 
            ('category', u'Desserts'), 
            ('id', 1)
        ])]
        self.assertEqual(response_filter.status_code, status.HTTP_200_OK)
        self.assertEqual(response_filter.data, expected_output)


        # ------------------------------------------------------------
        # Let's delete the truck:
        url = "%s%s/" % (URL_ROOT, id) 
        response_delete = self.client.delete(url, format='json')
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        

        # ------------------------------------------------------------
        # Let's get now all the trucks and check it is now empty list
        response_all = self.client.get(URL_ROOT, format='json')
        self.assertEqual(response_all.status_code, status.HTTP_200_OK)
        self.assertEqual(response_all.data, [])


        # ------------------------------------------------------------
        # Let's get now the item 1: should return a not found status
        url = "%s%s/" % (URL_ROOT, id) 
        response_item = self.client.get(url, format='json')
        self.assertEqual(response_item.status_code, status.HTTP_404_NOT_FOUND)
