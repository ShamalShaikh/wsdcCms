from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from conference.models import *
from login_auth.models import *
from manager.models import *
import datetime

# Create your views here.
def index(request,alias):
	conference = Conference.objects.get(conference_alias=alias)
	response = {}
	response['conference']=conference
	response['alias']=alias
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images
	try :
		payment = Payment.objects.get(user=request.user, conf_id=conference)
		response['payment']=payment
		if payment is not None :
			papers = {}
			try :
				papers = Conf_Paper.objects.filter(uid=request.user, conf_id=conference)
				response['papers']=papers
				return render(request,'conference/conference.djt',response)
			except :
				return render(request,'conference/conference.djt',response)
		else :
			return render(request,'conference/conference.djt',response)
	except :
		return render(request,'conference/conference.djt',response)

@login_required(login_url='/signin')
def make_payment(request,alias):
	conference = Conference.objects.get(conference_alias=alias)
	return render(request,'conference/payment.djt',{'conference':conference})

@login_required(login_url='/signin')
def payment(request,alias):
	if request.method == 'POST' :
		dd_pic = request.FILES['dd_file']
		id_pic = request.FILES['id_file']
		user = request.user
		conf_id = Conference.objects.get(conference_alias=alias)
		amount = 0

		previousPayment = Payment.objects.filter(user=request.user,conf_id=conf_id)
		print previousPayment
		if len(previousPayment)==1:
			previousPayment[0].pic_of_dd = dd_pic
			previousPayment[0].pic_of_id = id_pic
			previousPayment[0].is_rejected = False
			previousPayment[0].remarks = ""
			previousPayment[0].save()
		else:
			pay = Payment()
			pay.amount = amount
			pay.user = user
			pay.conf_id = conf_id
			pay.pic_of_dd = dd_pic
			pay.pic_of_id = id_pic
			pay.is_approved = False
			pay.payment_mode = 'dd'
			pay.save()
		url = '/conference/'+alias
		return redirect(url)
	return render(request,'conference/payment.djt',{'conference':conference})

@login_required(login_url='/signin')
def upload_paper(request,alias):
	conference = Conference.objects.get(conference_alias=alias)
	now = datetime.datetime.now()
	if request.method == 'POST' :
		regconf = None
		try:
			regconf = Registered_Conference.objects.get(conf_id=conference,user=request.user)
		except:
			regconf = Registered_Conference()
			regconf.conf_id = conference
			regconf.user = request.user
			regconf.save()
		if regconf.papers.count() < conference.max_papers:
			paper = Conf_Paper()
			paper.conf_id=conference
			paper.uid=request.user
			paper.paperfile=request.FILES['paper_file']
			paper.papername=request.POST['paper_name']
			paper.submissionDate=now.strftime("%Y-%m-%d")
			paper.save()
			regconf.papers.add(paper)
			regconf.save()
	url = '/conference/'+conference.conference_alias+"/dashboard/"
	return redirect(url)

@login_required(login_url='/signin')
def dashboard(request,alias):
	response = {}
	response['alias']=alias
	conference = Conference.objects.filter(conference_alias=alias)[0]
	conferences = Registered_Conference.objects.filter(user=request.user)
	payments = Payment.objects.filter(user=request.user)
	response['conference']= conference
	response['conferences'] = conferences
	response['payments'] = payments
	papers = {}
	finalpapers = {}
	try :
		papers = Conf_Paper.objects.filter(uid=request.user, conf_id=conference)
	except:
		papers = {}
	if len(papers) < conference.max_papers:
		response['upload_paper'] = True
	else:
		response['upload_paper']=False 
	response['papers']=papers

	for paper in papers:
		print paper.paper_id
		try:
			finalpaper = Final_paper.objects.filter(related_paper__paper_id=paper.paper_id)
			finalpapers += finalpaper
		except:
			print "No final paper for this yet"

	print finalpapers
	response['finalpapers'] = finalpapers
			
	if len(finalpapers) < conference.max_papers:
		response['final_paper'] = True
	else:
		response['final_paper'] = False

	if request.method == 'POST':
		u = User.objects.get(username=request.user.username)
		u.first_name = request.POST['firstname']
		u.last_name = request.POST['lastname']
		u.email = request.POST['email']
		u.username = request.POST['username']

		try:
			u.save()
			response['message'] = "Details Updated"
			return HttpResponseRedirect('/profile/3/')
		except:
			response['message'] = "Username already exists"
			return render(request, 'login_auth/sites/profile.djt',response)

	return render(request, 'conference/upload_paper.djt',response)

def treat(request):
	conference = Conference.objects.get(conference_alias='treat17')
	response = {}
	response['conference']=conference
	response['alias']='treat17'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment

	return render(request, 'conference/treat/treat.djt',response)

def treatabout(request):
	conference = Conference.objects.get(conference_alias='treat17')
	response={}
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/treat/about.djt',response)

def treatlinks(request):
	conference = Conference.objects.get(conference_alias='treat17')
	response={}
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/treat/links.djt',response)

@login_required(login_url='/signin')
def reupload_paper(request,alias):
	conference = Conference.objects.get(conference_alias=alias)
	now = datetime.datetime.now()
	if request.method == 'POST' :
		paper = Conf_Paper.objects.get(paper_id=request.POST['paperid'],uid=request.user)
		paper.paperfile=request.FILES['paper_file']
		paper.submissionDate=now.strftime("%Y-%m-%d")
		paper.save()
	url = '/conference/'+conference.conference_alias+"/dashboard/"
	return redirect(url)	

@login_required(login_url='/signin')
def final_paper(request,alias):
	conference = Conference.objects.get(conference_alias=alias)
	now = datetime.datetime.now()
	if request.method == 'POST' :
		papername = request.POST['paper_name']
		paper = Conf_Paper.objects.get(paper_id=request.POST['paper'],uid=request.user)
		copyright_form = request.FILES['copyright_form']
		final_paper = request.FILES['final_paper']

		finalpaper = Final_paper()
		finalpaper.papername = papername
		finalpaper.related_paper = paper
		finalpaper.final_file = final_paper
		finalpaper.copyright_form = copyright_form
		finalpaper.save()

	url = '/conference/'+conference.conference_alias+"/dashboard/"
	return redirect(url)
