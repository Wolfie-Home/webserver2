"""wolfie_home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views, api

urlpatterns = [
    url(r'^admin/', admin.site.urls), 
    url(r'^$', views.index, name='index'),
    url(r'^house$', views.house, name='house'),


    # ajax
    url(r'^api/login$', api.login, name='login'),
    url(r'^api/logout$', api.logout, name='logout'),
    url(r'^api/house$', api.house, name='devices'),
    url(r'^api/control$', api.control, name='control'),
    url(r'^api/module$', api.module, name='module')
]
