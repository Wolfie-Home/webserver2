from django.http import HttpResponse


def login(request):
    return HttpResponse("from login")

def logout(request):
    return HttpResponse("from logout")

def devices(request):
    return HttpResponse("from devices")

def control(request):
    return HttpResponse("from control")
