from django.shortcuts import render


# Create your views here.

from django.http import HttpResponse
from django.template import loader

from .models import Conference, Page


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

    num = Page.objects.get(cid=conference.cid, pageUrl='home')

    context = {
        'conference' : conference,
        'subpage' : num if not num else None,
        'navbar'  : Page.objects.filter(cid=conference.cid) if Page.objects.filter(cid=conference.cid).count() != 0 else None,
    }
    return HttpResponse(template.render(context, request))
    #return HttpResponse('This is conf homepage of ' + conferenceAlias)

def subpage(request, conferenceAlias, subpage):
    conference = Conference.objects.get(alias=conferenceAlias)
    template = loader.get_template('conferences/subpage.html')

    context = {
        'conference' : conference,
        'subpage' : Page.objects.get(cid=conference.cid, pageUrl=subpage),
        'navbar'  : Page.objects.filter(cid=conference.cid),
    }
    return HttpResponse(template.render(context, request))
    #return HttpResponse('We are on the subpage '+ subpage+ ' of the conf '+conferenceName)
