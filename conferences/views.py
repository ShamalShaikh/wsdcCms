from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
    return HttpResponse('Upcoming confe <br> Recent confs')

def home(request, conferenceName):
    return HttpResponse('This is conf homepage of ' + conferenceName)

def subpage(request, conferenceName, subpage):
    return HttpResponse('We are on the subpage '+ subpage+ ' of the conf '+conferenceName)
