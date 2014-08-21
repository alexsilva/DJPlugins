# Create your views here.
from django.http import HttpResponse


def say_hello(request):
    return HttpResponse("Hello from " + __name__)