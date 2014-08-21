from django.conf.urls import patterns, include, url

from admin.sites import AdminSite, PublicSite
from django.contrib import admin

admin.site = AdminSite()
publicSite = PublicSite()

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^site/', include(publicSite.urls)),

    url(r'^plugins/', include("plugins.urls")),
)

from django.conf import settings

# configuring the object
settings.PLUGIN_SETTINGS(globals())

# urls patterns settings
settings.PLUGIN_SETTINGS.set_urlpatterns()