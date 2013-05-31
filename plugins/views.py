# Create your views here.
from django.http import HttpResponse

from validate import exists
from django.conf import settings

def exists(request, app_name):
    return HttpResponse("<p>SETTINGS::INSTALLED_APPS %s = %s</p>" % (
            app_name, (app_name in settings.INSTALLED_APPS))
        )