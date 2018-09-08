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
		designation = request.POST['designation']
		qualification = request.POST['qualification']
		alumani = request.POST.get('alumaniCheck','off')
		print request.POST

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
				if(alumani == 'on'):
					alumani = Alumani()
					alumani.degree = request.POST['degree']
					alumani.year = request.POST['brach']
					alumani.branch = request.POST['yearPass']
					alumani.save()
					userprofile.alumani = alumani
				userprofile.save()
				response['message'] = "Successfully Registered"
				return render(request,'login_auth/sites/login.djt',response)
			except :
				response['message'] = "username already exist"
				return render(request,'login_auth/sites/register.djt',response)
	return render(request,'login_auth/sites/register.djt',response)

def registerSpons(request,alias):
	response={}
	response['alias'] = alias
	if request.method=='POST':
		print request.POST
		conf = Conference.objects.get(alias = alias)
		orgname = request.POST['orgname']
		orgType = request.POST['orgType']
		mc_ccd = request.POST['mc_ccd']
		addr1 = request.POST['addr1']
		addr2 = request.POST['addr2']
		email = request.POST['email']
		contact = request.POST['contact']
		sponsCategory = request.POST['sponsCategory']
		if request.FILES:
			advertFile = request.FILES['advertFile']
		
		numDelegates = request.POST['numDelegates']
		username = request.POST['username']
		password1 = request.POST['password']
		password2 = request.POST['confirm_password']

		if password1 != password2 :
			response['message'] = "Password doesn't match"
			return render(request,'login_auth/sites/register.djt',response)
		else :
			user = User()
			user.first_name = orgname
			# user.last_name = lastname
			user.username = username
			user.email = email
			user.set_password(password1)
			try:
				user.save()
			except :
				response['message'] = "username already exist"
				return render(request,'login_auth/sites/register.djt',response)
			sponsprofile = SponsorProfile()
			sponsprofile.user = user
			sponsprofile.conf = conf
			sponsprofile.orgName = orgname
			sponsprofile.orgType = orgType
			sponsprofile.md_cco = mc_ccd
			sponsprofile.address1 = addr1
			sponsprofile.address2 = addr2
			sponsprofile.contact = contact
			sponsprofile.category = sponsCategory
			if request.FILES:
				sponsprofile.advertisement = advertFile
			sponsprofile.save()

			print "spons save"
			# Now save all delegates
			for i in range(1,int(numDelegates) + 1):
				delegatename = request.POST['delegatename' + str(i)]
				delegeate = request.POST['delegeate' + str(i)]
				delegatecontact = request.POST['delegatecontact' + str(i)]
				delegateemail = request.POST['delegateemail' + str(i)]
				print delegatename
				delegate = Delegates(sponsor = sponsprofile,
									name = delegatename,
									delegate = delegeate,
									contact = delegatecontact,
									email = delegateemail)
				delegate.save()
			response['message'] = "Successfully Registered"
			return render(request,'login_auth/sites/login.djt',response)
			
	return render(request,'login_auth/sites/registerSpons.djt',response)
			
def signin(request,alias):
	response={}
	response['alias'] = alias
	print "ok"
	print alias
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