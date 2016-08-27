from django.shortcuts import render


# Create your views here.

from django.http import HttpResponse
from django.template import loader

from .models import Conference


def index(request):
    conference = Conference.objects.all()
    template = loader.get_template('conferences/main.html')
    context = {
        'upcoming_confs' : Conference.objects.filter(status='U'),
        'recent_confs' : Conference.objects.filter(status='P'),

    }
    return HttpResponse(template.render(context, request))

    #return HttpResponse('Upcoming confe <br> Recent confs')

def home(request, conferenceAlias):
    conference = Conference.objects.get(alias=conferenceAlias)
    template = loader.get_template('conferences/conference.html')
    context = {
        'conference' : conference,
    }
    return HttpResponse(template.render(context, request))
    #return HttpResponse('This is conf homepage of ' + conferenceAlias)

def subpage(request, conferenceAlias, subpage):
    return HttpResponse('We are on the subpage '+ subpage+ ' of the conf '+conferenceName)
