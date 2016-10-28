from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from conference.models import Conference, Conf_Paper
from reviews.models import Reviewer, Questions, Answers

def index(request):
	return redirect('/manager/sigin/')

def sigin(request):
	return render(request,'')

def home(request):
	return render(request, 'manager/home.djt', {})

def assign_reviewer(request, paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	reviewer = Reviewer.objects.all().exclude(papers=paper)
	reviewer_assigned = Reviewer.objects.filter(papers=paper)


	context = {
		'reviewer':reviewer,
		'reviewer_assigned':reviewer_assigned,
		'paper':paper,
	}
	return render(request, 'manager/assignreviewer.djt', context)

def reviewCompleted(request,paper_id,u_id):
	reviewer = Reviewer.objects.get(id=u_id)
	questions = Questions.objects.filter(paper_id = paper_id)
	answers = Answers.objects.filter(reviewer=reviewer)
	
	print questions

	context = {
		'answers':answers,
		'questions':questions,
	}

	return render(request, 'manager/reviewresp.djt', context)