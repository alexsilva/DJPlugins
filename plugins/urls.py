from django.conf.urls import patterns, url

urlpatterns = patterns('plugins',
    url(r'^app/(.*)', "views.exists"),
)