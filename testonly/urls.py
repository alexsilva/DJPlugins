from django.conf.urls import patterns, include, url

urlpatterns = patterns('testonly',
    url(r'', "views.say_hello"),
)