from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse,HttpResponseForbidden
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from login_auth.models import Registered_Conference, Payment
from conference.models import Conference
from login_auth.models import *
from sendfile import sendfile


@login_required(login_url='/signin/mmse2018')
def dddownload(request, payment_id):
	p = Payment.objects.get(id=payment_id)
	if not request.user.is_superuser and request.user != p.user:
		return HttpResponseForbidden('Sorry, you cannot access this file')
	return sendfile(request, p.pic_of_dd.path)

@login_required(login_url='/signin/mmse2018')
def iddownload(request, payment_id):
	p = Payment.objects.get(id=payment_id)
	if not request.user.is_superuser and request.user != p.user:
		return HttpResponseForbidden('Sorry, you cannot access this file')
	return sendfile(request, p.pic_of_id.path)

@login_required(login_url='/signin/mmse2018')
def rejectedpaymentdownload(request, rej_payment_id):
	p = Rejected_payment.objects.get(id=rej_payment_id)
	if not request.user.is_superuser and request.user != p.user:
		return HttpResponseForbidden('Sorry, you cannot access this file')
	return sendfile(request, p.pic_of_dd.path)

# Create your views here.
# def index(request):
# 	return redirect('/dashboard')

def Register(request,alias):
	if request.user.is_authenticated():
	    return redirect('/dashboard/'+alias)
	return render(request,'login_auth/sites/register.djt',{'alias':alias})

def register(request,alias):
	response={}
	response['alias'] = alias
	if request.method=='POST':
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		password1 = request.POST['password']
		password2 = request.POST['confirm_password']
		username = request.POST['username']
		email = request.POST['email']
		institute = request.POST['institute']
		department = request.POST['department']
		conact = request.POST['contact']
		gender = request.POST['gender']
		if password1 != password2 :
			response['message'] = "Password doesn't match"
			return render(request,'login_auth/sites/register.djt',response)
		else :
			user = User()
			user.first_name = firstname
			user.last_name = lastname
			user.username = username
			user.email = email
			user.set_password(password1)
			try:
				user.save()
				userprofile = UserProfile()
				userprofile.user = user
				userprofile.institute = institute
				userprofile.department = department
				userprofile.contact = conact
				userprofile.gender = gender
				userprofile.save()
				response['message'] = "Successfully Registered"
				return render(request,'login_auth/sites/login.djt',response)
			except :
				response['message'] = "username already exist"
				return render(request,'login_auth/sites/register.djt',response)
	return render(request,'login_auth/sites/register.djt',response)
			
def signin(request,alias):
	response={}
	response['alias'] = alias
	if request.user.is_authenticated():
	    return redirect('/dashboard/'+alias)
	if request.method == "POST":
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(username=username, password=password)
	    if user is not None:
	        login(request, user)
	        return redirect('/dashboard/'+alias)
	    else:
	        response['message']='User is not registered/Password Incorrect' 
	return render(request,'login_auth/sites/login.djt',response)

def signout(request,alias):
	logout(request)
	return redirect('/dashboard/'+alias)

def dashboard(request,alias):
	response={}
	# response['conferences'] = Conference.objects.filter(is_published=True)	
	# return render(request,'login_auth/sites/dashboard.djt',response)
	return redirect('/conference/'+alias)


@login_required(login_url='/signin')
def profile(request,type):
	response = {}

	conferences = Registered_Conference.objects.filter(user=request.user)
	payments = Payment.objects.filter(user=request.user)
	response['conferences'] = conferences
	response['payments'] = payments
	response['type'] = type

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

	return render(request, 'login_auth/sites/profile.djt',response)