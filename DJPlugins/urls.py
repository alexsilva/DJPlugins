from django.conf.urls import patterns, include, url
from admin.sites import AdminSite, PublicSite

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

# Creating two objects websites. but their behavior will be different.
# The need to rewrite the admin site is in fact apply plugins on it.
admin.sites.site = admin.site = AdminSite()
publicSite = PublicSite()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^site/', include(publicSite.urls)),

    url(r'^plugins/', include("plugins.urls")),
)

from django.conf import settings

# configuring the object
settings.PGL_SETTINGS(locals())

# urls patterns settings
settings.PGL_SETTINGS.set_urlpatterns()