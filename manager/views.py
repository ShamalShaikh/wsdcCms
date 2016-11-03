from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from conference.models import Conference, Conf_Paper
from reviews.models import Reviewer, Questions, Answers
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

def signout(request):
	logout(request)
	return redirect('/manager/signin')

@login_required(login_url='/manager/signin/')
def home(request):
	manager = Manager.objects.get(user=request.user)
	conferences = Conference.objects.filter(manager=manager)
	return render(request, 'manager/home.djt', {'conferences':conferences})

@login_required(login_url='/manager/signin/')
def assign_reviewer(request, paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	reviewer = Reviewer.objects.all().exclude(papers=paper)
	reviewer_assigned = Reviewer.objects.filter(papers=paper)
	if paper.is_approved:
		paper.under_review = False
	elif paper.is_rejected:
		paper.under_review = False
	else:
		paper.under_review = True
	paper.save()
	context = {
		'reviewer':reviewer,
		'reviewer_assigned':reviewer_assigned,
		'paper':paper,
		'is_approved':paper.is_approved,
		'is_rejected':paper.is_rejected,
		'under_review':paper.under_review,
	}
	return render(request, 'manager/assignreviewer.djt', context)

@login_required(login_url='/manager/signin/')
def conference_landing(request,cid,type):
	conference = Conference.objects.get(conference_id=cid)
	regconfs = Registered_Conference.objects.filter(conf_id=conference)
	users = []
	paidtrans = []
	pending_dds= []
	papers = []
	for regconf in regconfs:
		user = regconf.user
		payment = Payment.objects.get(user=user,conf_id=conference)
		users.append(user)
		paidtrans.append(payment)
		for paper in regconf.papers.all() :
			papers.append(paper)


	for pendingtrans in Payment.objects.filter(conf_id=conference):
		if pendingtrans.is_approved==False :
			pending_dds.append(pendingtrans)

	response={}
	response['users']=users
	response['paidtrans']=paidtrans
	response['papers']=papers
	response['pending_dds']=pending_dds
	response['type']=type
	response['conference']=conference
	return render(request,'manager/conf_navbar.djt',response)

def reviewerAssigned(request, paper_id, u_id):
	reviewer = Reviewer.objects.get(id=u_id)
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	reviewer.papers.add(paper)
	reviewer.save()
	return HttpResponse("done")

def reviewCompleted(request,paper_id,u_id):
	reviewer = Reviewer.objects.get(id=u_id)
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	answers = Answers.objects.filter(reviewer=reviewer).filter(paper=paper)
	ans_len = len(answers)
	print paper
	answers = Answers.objects.filter(reviewer=reviewer)

	context = {
		'ans_len':ans_len,
		'answers':answers,

	}
	return render(request, 'manager/reviewresp.djt', context)

def averageResponses(request, paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	conf = paper.conf_id
	questions = Questions.objects.filter(conference=conf)
	avg = []
	for q in questions:
		ans = q.answers_set.filter(paper=paper)
		sum=0
		count=0
		for i in ans:
			sum = sum+int(i.answer)
			count = count+1
		if count>0:
			average = sum/count
			avg.append(average)
		else:
			avg.append(0)
	context = {
		'questions':questions,
		'avg':avg,
		'paper':paper,
	}
	return render(request, 'manager/allresponses.djt', context)

@login_required(login_url='/manager/signin/')
def approve_payment(request,payid):
	payment = Payment.objects.get(id=payid)
	payment.is_approved=True
	payment.is_rejected=False
	payment.save()
	regconf = Registered_Conference()
	regconf.user = payment.user
	regconf.conf_id = payment.conf_id
	regconf.save()
	print regconf.conf_id.conference_id
	url = '/manager/conference_landing/'+str(regconf.conf_id.conference_id)+'/1/'
	return redirect(url)

def disapproval(request):
	if request.method=='POST':
		print request.POST['remark']
		print request.POST['payid']
		payment=Payment.objects.get(id=request.POST['payid'])
		payment.remarks=request.POST['remark']
		payment.is_rejected = True
		payment.save()
	return redirect('/manager/conference_landing/2/1')


def questionnaire(request,cid):
	conference = Conference.objects.get(conference_id=cid)


	response={}
	response['message'] = "Add your questions below for the conference "+conference.conference_name
	if request.method == "POST":
		try:
			i = 1
			while ('question' + str(i)) in request.POST:

				newQuestion = request.POST['question'  + str(i)]
				if newQuestion != "":
					if request.POST['qId' + str(i)] == "":
						q = Questions()
						q.conference = conference
					else:
						q = Questions.objects.get(id=request.POST['qId' + str(i)])
					q.question = newQuestion

					q.save()
					i += 1
					response['message'] = "Question saved successfully!"
				else:
					response['message'] = "Question body cannot be empty. Please try again."
		except:
			response['message'] = "Error in saving the question. Please try again."


	questions = Questions.objects.filter(conference=conference)
	q_len = len(questions)

	response['questions'] = questions
	response['conference'] = conference
	response['q_len'] = q_len

	return render(request,'manager/questionnaire.djt',response)


def isApprovedPaper(request, paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	paper.is_approved = True
	paper.is_rejected = False
	paper.under_review = False
	paper.save()
	return HttpResponseRedirect('/manager/assignreviewer/'+paper_id+'/')

def isDisapprovedPaper(request, paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	paper.is_approved = False
	paper.is_rejected = True
	paper.under_review = False
	paper.save()
	return HttpResponseRedirect('/manager/assignreviewer/'+paper_id+'/')
