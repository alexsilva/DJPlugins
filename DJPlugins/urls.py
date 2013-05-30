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
#
from plugins.models import App
from plugins.validate import app_exists

for app in App.objects.all():
    if app_exists(app.name):
        print "LOG: urls:add-prefix %s"%app
        urlpatterns += (
            url(app.prefix, include(app.name + ".urls")),
        )
    else:
        print "LOG: urls:add-prefix app not found %s"%app