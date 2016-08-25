from django.conf.urls import url
from django.http import HttpResponse, JsonResponse
from django.template import loader

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(None, request))
    

urlpatterns = [
    url(r'^$', index),
]
