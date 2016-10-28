from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from conference.models import Conference
from reviews.models import Reviewer
from manager.models import *

def signin(request):
	return render(request,'login_auth/sites/manager_signin.djt')

def signin_auth(request):
	reponse={}
	username = request.POST['username']
	user = User.objects.get(username=username)
	manager = Manager.objects.get(user=user)
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
	return render(request,'login_auth/sites/manager_signin.djt',response)

def home(request):
	return render(request, 'manager/home.djt', {})

def assign_reviewer(request):
	reviewer = Reviewer.objects.all()
	context = {
		'reviewer':reviewer,
	}
	return render(request, 'manager/assignreviewer.djt', context)
