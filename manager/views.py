from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from conference.models import Conference
from reviews.models import Reviewer
from manager.models import *
from login_auth.models import *

def signin(request):
	return render(request,'login_auth/sites/manager_signin.djt')

def signin_auth(request):
	response={}
	username = request.POST['username']
	user = User.objects.get(username=username)
	manager = Manager.objects.filter(user=user)
	if request.user.is_authenticated() and manager:
	    return redirect('/manager')
	if request.method == "POST" and manager:
	    password = request.POST['password']
	    user = authenticate(username=username, password=password)
	    if user is not None:
	        login(request, user)
	        return redirect('/manager')
	    else:
	        response['message']='User is not registered/Password Incorrect'
	if not manager:
		response['message']='Only Manager can Login'
	return render(request,'login_auth/sites/manager_signin.djt',response)

@login_required(login_url='/manager/signin/')
def home(request):
	conferences = Conference.objects.filter(manager=request.user)
	return render(request, 'manager/home.djt', {'conferences':conferences})

@login_required(login_url='/manager/signin/')
def assign_reviewer(request):
	reviewer = Reviewer.objects.all()
	context = {
		'reviewer':reviewer,
	}
	return render(request, 'manager/assignreviewer.djt', context)

@login_required(login_url='/manager/signin/')
def conference_landing(request,cid,type):
	conference = Conference.objects.get(conference_id=cid)
	regconfs = Registered_Conference.objects.filter(conf_id=conference)
	users = []
	pending_dds= []
	papers = []
	for regconf in regconfs:
		user = regconf.user
		papers.append(regconf.papers.all())
		payment = Payment.objects.filter(user=user)
		if payment.is_aprooved:
			users.append(user)
		else:
			pending_dds.append(payment)
	response={}
	response['users']=users
	response['papers']=papers
	response['pending_dds']=pending_dds
	response['type']=type
	return render(request,'manager/conf_navbar.djt',response)

