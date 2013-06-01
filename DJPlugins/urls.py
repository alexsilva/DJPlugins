from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^plugins/', include("plugins.urls")),
)

from django.conf import settings

# configuring the object
settings.PGL_SETTINGS(locals())

# urls patterns settings
settings.PGL_SETTINGS.set_urlpatterns()