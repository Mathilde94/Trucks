# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.views.generic import TemplateView, View, DetailView

from truck.models import Truck

def index(request):
    """
    Get the main page 

    Load the main index.html template and fetch the categories
    from all the trucks

    :return: HttpResponse of the template index.html with the
            correct categories
    """

    template = loader.get_template('website/index.html')

    data = {'categories': ['All'] + 
            [str(cat[0]) for cat in get_categories()]}
    
    context = RequestContext(request, data)

    return HttpResponse(template.render(context))

def get_categories():
    """
    Get all the possible categories

    :return: The list of all the possible categories and their occurence
    in alphabetic order.
    """

    trucks = Truck.objects.all()
    categories = {}

    for truck in trucks:
        category = truck.category.lower()

        if category == '':
            continue

        if category not in categories.keys():
            categories[category] = 0

        categories[category] += 1

    categories = [ (category, categories[category]) for category in categories.keys()]
    categories.sort(key=lambda x:x[0])

    categories = [(upperFirstLetter(cat[0]), cat[1]) for cat in categories]

    return categories
    

def upperFirstLetter(string):
    """
    Get the First Letter of a word in uppercase

    :return: The new string
    """
    return "".join([ string[0].upper(), string[1:]])
