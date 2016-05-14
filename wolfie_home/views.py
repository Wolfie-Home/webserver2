from django.http import HttpResponse
from django.template import loader


def index(request):
    index_template = loader.get_template('wolfie_home/login.html')
    return HttpResponse(index_template.render(None, request))


def house(request):
    index_template = loader.get_template('wolfie_home/house.html')
    return HttpResponse(index_template.render(None, request))


def message(request):
    resp = HttpResponse()
    if not request.GET.has_key('message') or not request.GET.has_key('message_type'):
        resp.status_code = 400
        return resp

    msg = request.GET['message']
    msg_t = request.GET['message_type']
    context = {
        'message': msg,
        'type': msg_t,
    }
    index_template = loader.get_template('wolfie_home/message.html')
    return HttpResponse(index_template.render(context, request))
