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
def make_payment(request):
	cid = request.GET['cid']
	conference = Conference.objects.get(conference_id=cid)
	return render(request,'conference/payment.djt',{'conference':conference})

@login_required(login_url='/signin')
def payment(request):
	cid = request.GET['cid']
	conference = Conference.objects.get(conference_id=cid)
	if request.method == 'POST' :
		dd_pic = request.FILES['dd_file']
		user = request.user
		conf_id = Conference.objects.get(conference_id=cid)
		amount = request.POST['amount']

		previousPayment = Payment.objects.filter(user=request.user,conf_id=conference)
		print previousPayment
		if len(previousPayment)==1:
			previousPayment[0].pic_of_dd = dd_pic
			previousPayment[0].is_rejected = False
			previousPayment[0].remarks = ""
			previousPayment[0].save()
		else:
			pay = Payment()
			pay.amount = amount
			pay.user = user
			pay.conf_id = conf_id
			pay.pic_of_dd = dd_pic
			pay.is_approved = False
			pay.payment_mode = 'dd'
			pay.save()
		url = '/conference/?cid='+cid
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
	try :
		papers = Conf_Paper.objects.filter(uid=request.user, conf_id=conference)
	except:
		papers = {}
	if len(papers) < conference.max_papers:
		response['upload_paper'] = True
	else:
		response['upload_paper']=False 
	response['papers']=papers
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

