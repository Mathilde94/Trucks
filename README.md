Food Trucks
===========

What does it do - UX
--------------------

### What is the problem
This application is about showing the Trucks Categories	that you can find near any specific location on a	map.
The data available is located here: https://data.sfgov.org/Permitting/Mobile-Food-Facility-Permit/rqzj-sfat.
It is mostly containing trucks that are located in the SF area. This is a Full Stack Application.

### Assumptions

1) The user is based in San Francisco, or its close areas.

2) The data in data.sfgov.org for the "Mobile Food Facility Permit" is up to date.

3) For the purpose of this application, I took the assumptions that trucks are not added
   or removed too frequently: it is easy to add a new truck (with the API created, see below).

4) The user can choose any location on a map to check the types of Trucks near it.


### Main Features for the User

This will be an interface where the user can select easily:

1) A location on a map (a default one would be already there, center of SF).

2) [Optional] A type of category (all types by default).

3) [Optional] A maximum distance he is willing to walk (1 mile by default)

The interface will then show the list of trucks categories he cn find close to the 
location selected, as well as the list of Trucks names in a section below.

### UX Decisions

We would want then to have:

1) A Map with SF as center. We do not want to have a too big or low zoom, something that a user could
   walk reasonably to for a lunch for instance (1mile or 2 miles radius). You can as well change the 
   center/location to look for with a right click and an option appearing to check this new location 
   (we need to specify this action somewhere as well). 
   This map would also show the trucks that are closed to this location (filtered by category chose 
   by the user, see below). Each truck would be represented by a Marker, that if you click on it, you 
   should see the name of it.    

2) A div to select an optional category and the maximum distance willing to walk. Both of these values have a default
   of "All" categories and "1" radius mile.

3) A div giving the result of the different categories of Trucks this user can find around that specific location.

4) A place to show the list of trucks that respond to the criteria chose by default or by the user. This
   list would be in a div, showing also the number of trucks that correspond to the criteria. Passing over
   a div container of a truck, you should be able to see the truck location on the map (marker would change
   color) and the name and category of it


Choices of Backend
------------------

The main environment I decided to use is AWS.

### Architecture
This application would not have lots of users now and will still at start stage.
But, if that was not the case, I think placing a django application in a Docker environment, 
that we put on an Elastic Beanstalk Service on AWS, that would generate the scale up/down service, would be 
a good start. We would then map a DNS3 record to the Elastic Load Balancer of this cluster of machines.

For now, and as I used AWS on my own account, I will use a simple EC2 machine.

### Database
As this application is still for small use, I would use a simple sqlite DB on this EC2 machine that Docker
would use.

AWS allows you to have specific databases that you can ensure safety with replication etc. 
There are a lot of options of DB there: https://aws.amazon.com/running_databases/.

This databases not free, I put for now the database in the AWS EC2 instance as a simple sqlite3 DB.
You can generate the content of this database as well, from the data located at the URL above. There
is a python script on databases/generate.py that does this.

### Framework
My favorite MVC framework I generally use is Django, written in my favorite Language, Python.

### REST API Framework
Django has a REST API framework that I wanted to learn on this project. I decided to use
it. This REST API framework will allow GET requests on the list of Trucks. It will read the trucks on Database, 
allow to perform some filtering as parameters you specify.

You can filter a GET request with the latitude/longitude of a location you want, the category and the radius.
The category and radius have defaults ("ALL" categories, "radius" minimum to 2 miles) and the location to the center
of San Francisco. I had to also write a part where you filter the trucks that are close to a location based on the 
mathematical distance with latitude/longitude.

In the production environment, you can block the requests to only GET, but for a developer, 
on your personal environment, you can as well do a PUT, POST. 

The page to access directly the UI interface on your personal development can be here: http://localhost/api/trucks.
This page can be blocked when you are in production, where you would jst return for example a simple JSON. You can 
set up this as I have on Trucks/settings.py:

     'REST_FRAMEWORK': { ...
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticatedOrReadOnly'
        ]
     }


### REST API Tests
The REST API framework has its own test that you can run in your development as below:
   
    python manage.py test truck

It will test when you add/put and delete a truck.


Choices for Front End
---------------------

### Backbone.js
As specified in the Front End paragraph, I chose the backbone.js framework. It is pretty well adapted for any
REST API framework and I decided to learn it with this project. The main script is in website/static/js/app.js where
a Truck Model and its View are defined, as well as the Truck Collection responding to the /api/trucks API and the
trucks View. Then, a few JS functions are defined to initialize the map/parameters of the UI, the right click on the map,
the updating of the view etc. 

### Selenium Django Tests
The UI is tested through the Selenum embedded in Django. The main tests are the UI interaction and result with 2 main
trucks, where you can see if updating the category will update correctly the list of the trucks, check the radius button. 
What is left here is to check the markers on the Map. 

To run the UI tests (you will need Firefox):

    python manage.py test website

You will see a Firefox window opening and buttons changing, meaning the tests are running :) 

Code generated
--------------
The main code generated is the basic Django (with the settings.py mostly where i just updated a few fields), and the
rest framework. The radius button is also from outside, even if adapted to fit the application.

Some JS libraries have been as well downloaded: the Backbone, undescore, jquery and gmaps.


Where Is It?
------------
I decided to put this website on this AWS EC2 instance: http://ec2-54-149-29-15.us-west-2.compute.amazonaws.com/. 
The code is located here: https://github.com/Mathilde94/Trucks.  

### A few indications in case you want to play around

On an Ubuntu machine, install Django, Django Rest Framework (with markdown and django-filter) and selenium. By doing a pip freeze:

```
    Django==1.8.3
    djangorestframework==3.1.3
    django-filter==0.10.0
    Markdown==2.6.2
    selenium==2.47.0
```

Copy the start/django on your /etc/init.d.
Update the settings.py with the path of your sqlite3.db (empty file is good).

Go to the git repository, generate the Database:

    python manage.py migrate
    python databases/generate.py rebuild

Once your environment is ready, execute:

    sudo service django start

Personal Information
--------------------
You can find my resume on Linkedin Here: https://www.linkedin.com/pub/mathilde-caron/38/a78/a48. 
I have an app engine blog here wit a few articles on some other projects I have been working on: http://mathildecaron94.appspot.com/.

My personal experiences on the tools are:
1) Python: 4/5 years (school, work, personal projects)
2) Django: 2 years (personal projects and work)
3) Backbone.js: basics, the time I spent doing this challenge.
4) Rest API Framework: a few days when I wanted to find out what it was, and this time spent on this challenge.
5) Selenium: I had a brief introduction of it before

I did this project on a week end and 2 evening scattered in the week to learn BackBone.js and Rest API Framework basics.
