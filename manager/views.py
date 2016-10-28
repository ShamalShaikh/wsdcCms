from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from conference.models import Conference
from reviews.models import Reviewer

def index(request):
	return redirect('/manager/sigin/')

def sigin(request):
	return render(request,'')

def home(request):
	return render(request, 'manager/home.djt', {})

def assign_reviewer(request):
	reviewer = Reviewer.objects.all()
	context = {
		'reviewer':reviewer,
	}
	return render(request, 'manager/assignreviewer.djt', context)


