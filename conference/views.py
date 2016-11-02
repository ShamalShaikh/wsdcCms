from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from conference.models import *
from login_auth.models import *
import datetime

# Create your views here.
@login_required(login_url='/signin')
def index(request):
	cid = request.GET['cid']
	conference = Conference.objects.get(conference_id=cid)
	try :
		print request.user
		payment = Payment.objects.get(user=request.user, conf_id=conference)
		print "payment found"
		if payment is not None :
			papers = {}
			try :
				print "papers"
				papers = Conf_Paper.objects.filter(uid=request.user, conf_id=conference)
				return render(request,'conference/conference.djt',{'conference':conference,'payment':payment,'papers':papers})
			except :
				print "no papers"
				return render(request,'conference/conference.djt',{'conference':conference,'payment':payment})
		else :
			return render(request,'conference/conference.djt',{'conference':conference})
	except :
		return render(request,'conference/conference.djt',{'conference':conference})

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

		previousPayment = Payment.objects.get(user=request.user,conf_id=conference)
		if previousPayment:
			previousPayment.pic_of_dd = dd_pic
			previousPayment.save()
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
def upload_paper(request,cid):
	conference = Conference.objects.get(conference_id=cid)
	now = datetime.datetime.now()
	if request.method == 'POST' :
		paper = Conf_Paper()
		paper.conf_id=conference
		paper.uid=request.user
		paper.paperfile=request.FILES['paper_file']
		paper.papername=request.POST['paper_name']
		paper.submissionDate=now.strftime("%Y-%m-%d")
		paper.save()

		regconf = Registered_Conference.objects.get(conf_id=conference,user=request.user)
		regconf.papers.add(paper)
		regconf.save()
	url = '/conference/?cid='+cid
	return redirect(url)