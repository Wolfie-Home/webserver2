from django.http import HttpResponse
from django.template import loader


def index(request):
    index_template = loader.get_template('wolfie_home/login.html')
    return HttpResponse(index_template.render(None, request))


def house(request):
    index_template = loader.get_template('wolfie_home/login.html')
    return HttpResponse(index_template.render(None, request))
