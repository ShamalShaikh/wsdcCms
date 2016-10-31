from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from conference.models import Conference

# Create your views here.
def index(request):
	return redirect('/Register/')

def Register(request):
	if request.user.is_authenticated():
	    return redirect('/dashboard')
	return render(request,'login_auth/sites/register.djt')

def register(request):
	response={}
	if request.method=='POST':
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		password1 = request.POST['password']
		password2 = request.POST['confirm_password']
		username = request.POST['username']
		email = request.POST['email']
		if password1 != password2 :
			reponse['message'] = "Password doesn't match"
			return render(request,'login_auth/sites/register.djt',reponse)
		else :
			user = User()
			user.first_name = firstname
			user.last_name = lastname
			user.username = username
			user.email = email
			user.set_password(password1)
			try:
				user.save()
				reponse['message'] = "Successfully Registered"
				return render(request,'login_auth/sites/login.djt',reponse)
			except :
				reponse['message'] = "username already exist"
				return render(request,'login_auth/sites/register.djt',reponse)
	return render(request,'login_auth/sites/register.djt')
			
def signin(request):
	response={}
	if request.user.is_authenticated():
	    return redirect('/dashboard')
	if request.method == "POST":
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(username=username, password=password)
	    if user is not None:
	        login(request, user)
	        return redirect('/dashboard')
	    else:
	        response['message']='User is not registered/Password Incorrect' 
	return render(request,'login_auth/sites/login.djt',response)

@login_required(login_url='/signin')
def dashboard(request):
	response={}
	response['conferences'] = Conference.objects.filter(is_published=True)
	return render(request,'login_auth/sites/dashboard.djt',response)
