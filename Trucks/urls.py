from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

                       url(r'api/', include('truck.urls')),
                       url(r'^$', include('website.urls')),
                       url(r'truck/', include('website.urls')),
)
