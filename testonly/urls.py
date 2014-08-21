from django.conf.urls import patterns, url

urlpatterns = patterns('testonly',
                       url(r'', "views.say_hello"),
)