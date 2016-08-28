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

    try:
        conference = Conference.objects.get(alias=conferenceAlias)
        template = loader.get_template('conferences/conference.html')

        num = Page.objects.get(cid=conference.cid, pageUrl='home')



        context = {
            'conference' : conference,
            'subpage' : num if num else None,
            'navbar'  : Page.objects.filter(cid=conference.cid).exclude(pageUrl='sidebar') if Page.objects.filter(cid=conference.cid).exclude(pageUrl='sidebar').count() != 0 else None,
        }

        try:
            num = Page.objects.get(cid=conference.cid, pageUrl='sidebar')
            if num:
                context['sidebar'] = Page.objects.get(cid=conference.cid, pageUrl='sidebar')
        except:
            pass
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('conferences/404.html')
        return HttpResponse(template.render({}, request))

    #return HttpResponse('This is conf homepage of ' + conferenceAlias)

def subpage(request, conferenceAlias, subpage):

    try:
        conference = Conference.objects.get(alias=conferenceAlias)
        template = loader.get_template('conferences/conference.html')


        context = {
            'conference' : conference,
        'subpage' : Page.objects.get(cid=conference.cid, pageUrl=subpage).exclude(pageUrl='sidebar'),
        'navbar'  : Page.objects.filter(cid=conference.cid).exclude(pageUrl='sidebar'),
        }

        num = Page.objects.get(cid=conference.cid, pageUrl='sidebar')
        if num:
            context['sidebar'] = Page.objects.get(cid=conference.cid, pageUrl='sidebar')


        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('conferences/404.html')

        try:
            context = {'conference' : Conference.objects.get(alias=conferenceAlias),}
        except:
            context = {}

        return HttpResponse(template.render(context, request))


    #return HttpResponse('We are on the subpage '+ subpage+ ' of the conf '+conferenceName)
