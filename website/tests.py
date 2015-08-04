"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

"""

from django.test import TestCase
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

# Libraries in order to add a container for the UI test
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from collections import OrderedDict
URL_ROOT='/api/trucks/'

class UITestsSelenium(LiveServerTestCase):
    """
    Class to test main UI functionalities of the index page
    """
    @classmethod
    def setUpClass(cls):
        super(UITestsSelenium, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(UITestsSelenium, cls).tearDownClass()

    def test_main_page(self):
        """
        This test function will:
        - Add into DB two trucks that have different categories
        - Open the main page
        - Check two trucks are shown in the list
        - Check their categories are added to the list of categories
        - Update one category
        - Check there is only one truck shown (the only one from the category chosen)
        - Set the radius length to 0 and test no trucks are shown

        TODO: get the tests of the map: checking the number of markers on the map
        """

        # ------------------------------------------------------------
        # Let's create two new trucks that are close to SF Marker
        data1 = {
            'applicant': "Truck 1",
            'latitude': 37.7854111, 
            'longitude': -122.41679,
            'category': "Cupcakes"
        }
        id = 1
        response = self.client.post(URL_ROOT, data1, format='json')
        data1.update({'id': id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data2 = {
            'applicant': "Truck 2",
            'latitude': 37.7874111, 
            'longitude': -122.41679,
            'category': "Burgers"
        }
        id = 2
        response = self.client.post(URL_ROOT, data2, format='json')
        data2.update({'id': id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        trucks = [data1, data2]

        # ------------------------------------------------------------
        # Let's check now the main UI Page
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        
        # Let's check if the elements below exist
        # If not, selenium will raise an error
        map_container_div = self.selenium.find_element_by_id("map_container")
        trucks_div = self.selenium.find_element_by_id("trucks_list")  
        get_trucks_div = self.selenium.find_element_by_id("getTrucks")        

        # ------------------------------------------------------------
        # Let's check if we can see the truck in the list and that the
        # total is set to 1
        trucks_div = self.selenium.find_element_by_id("trucks_list")
        total_div = trucks_div.find_element_by_id("total") 
        self.assertEqual(total_div.text, "Number of Trucks: 2")
        trucks_list_div = trucks_div.find_element_by_id("list")  
        children_trucks = trucks_list_div.find_elements_by_class_name('truckContainer')
        self.assertEqual(len(children_trucks), 2) 

        # ------------------------------------------------------------
        # Let's check that the number of categories is 2
        categories_div = self.selenium.find_element_by_id("categories_list")
        total_div = categories_div.find_element_by_id("total") 
        self.assertEqual(total_div.text, "Number of Categories: 2")
        categories_list_div = categories_div.find_element_by_id("list")  
        children_categories = categories_list_div.find_elements_by_class_name('categoryContainer')
        self.assertEqual(len(children_categories), 2) 
        
        # ------------------------------------------------------------ 
        # Let's check we have the trucks div
        for index in range(len(trucks)):
            truck_div = children_trucks[index]
            truck_li = truck_div.find_elements_by_tag_name('li')
            self.assertEqual(len(truck_li), 2)
            truck_name, truck_category = truck_li
            self.assertEqual(truck_name.text, trucks[index]['applicant'])
            self.assertEqual(truck_category.text, trucks[index]['category'])

        # ------------------------------------------------------------
        # Let's check the options present Cupakes...
        categories_select = get_trucks_div.find_element_by_tag_name('select')
        trucks.reverse()
        possible_options = ['All'] + [ truck['category'] for truck in trucks]
        options = categories_select.find_elements_by_tag_name('option')
        self.assertEqual(len(options), len(possible_options))
        for option, text in zip(options, possible_options):
            self.assertEqual(option.text, text)

        # ------------------------------------------------------------
        # Now, let's click on the first option and update the list
        # of trucks
        option_to_click = options[1]
        category_clicked = options[1].text
        option_to_click.click()
        button_update = get_trucks_div.find_element_by_id('getListTrucks')
        button_update.click()

        # ------------------------------------------------------------
        # Check now we have only one truck, the correct category one
        total_div = trucks_div.find_element_by_id("total") 
        self.assertEqual(total_div.text, "Number of Trucks: 1")
        children_trucks = trucks_list_div.find_elements_by_class_name('truckContainer')
        self.assertEqual(len(children_trucks), 1) 
        
        for index in range(len(children_trucks)):
            truck_div = children_trucks[index]
            truck_li = truck_div.find_elements_by_tag_name('li')
            self.assertEqual(len(truck_li), 2)
            truck_name, truck_category = truck_li
            self.assertEqual(truck_category.text, category_clicked)
        
        # ------------------------------------------------------------
        # Check when we set up the radius to 0
        radius = get_trucks_div.find_element_by_id('radius')
        self.selenium.execute_script("arguments[0].value = '0';", radius)
        button_update.click()
        children_trucks = trucks_list_div.find_elements_by_class_name('truckContainer')
        self.assertEqual(len(children_trucks), 0)

        # ------------------------------------------------------------
        # Let's check that the number of categories is now 0
        categories_div = self.selenium.find_element_by_id("categories_list")
        total_div = categories_div.find_element_by_id("total") 
        self.assertEqual(total_div.text, "Number of Categories: 0")
        categories_list_div = categories_div.find_element_by_id("list")  
        children_categories = categories_list_div.find_elements_by_class_name('categoryContainer')
        self.assertEqual(len(children_categories), 0) 
