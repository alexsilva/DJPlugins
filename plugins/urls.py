from django.conf.urls import patterns, include, url

urlpatterns = patterns('plugins',
    url(r'^app/(.*)', "views.exists"),
)