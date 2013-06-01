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
from plugins.validate import exists
from plugins.models import App
import logging

logger = logging.getLogger(settings.PGL_SETTINGS.get_logger_name())

for app in App.objects.all():
    if exists(app.name):
        logger.debug("URLS: regex-pattern::add %s"%app)

        urlpatterns += patterns('',
            url(app.prefix, include(app.name + ".urls")),
        )
    else:
        logger.debug("URLS: regex-pattern::app not found %s"%app)