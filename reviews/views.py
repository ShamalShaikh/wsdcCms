from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate,login,logout
from .models import *
from conference.models import *
from .forms import ReviewForm
import traceback
import sys
from sendfile import sendfile
from django.contrib.auth.models import User
import os

# Create your views here.

def checkuserifReviewer(user):
	user = Reviewer.objects.filter(user=user)
	if len(user)>0:
		return True
	else:
		return False

def paperdownload(request, paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	if Reviewer.objects.filter(user=request.user).count()==0 :
		return HttpResponseForbidden('Sorry, you cannot access this file')
	return sendfile(request, paper.paperfile.path)


@login_required(login_url='/review/login/')
@user_passes_test(checkuserifReviewer,login_url="/review/404/")
def reviewHome(request):
	response = {}
	user=request.user
	reviewer = Reviewer.objects.get(user = request.user)
	papers = reviewer.papers.all()
	response['papers'] = papers
	return render(request, 'reviewer/home.djt',response)

def reviewPaper(request,paper_id):
	response = {}
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	reviewer = Reviewer.objects.get(user=request.user)
	response['paper'] = paper

	answers = Answers.objects.filter(paper=paper,reviewer=reviewer)
	response['answers'] = answers

	if Remarks.objects.filter(paper=paper,reviewer=reviewer).count() > 0:
		response['remark'] = Remarks.objects.get(paper=paper,reviewer=reviewer)

	return render(request,'reviewer/reviewPaper.djt',response)

def assignMarks(request,ansid):
	response = {}
	ans = Answers.objects.get(id=ansid)
	if request.method == 'POST':
		if ans.question.que_type == 0 :
			ans.marks = request.POST['marks']
		if ans.question.que_type == 1 :
			ans.answer = request.POST['answer']
		ans.save()
	return redirect('/review/reviewPaper/'+str(ans.paper.paper_id))

def submitRemark(request,paper_id):
	response = {}
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	reviewer = Reviewer.objects.get(user=request.user)
	if request.method == 'POST' :
		if Remarks.objects.filter(paper=paper,reviewer=reviewer).count() > 0:
			remark = Remarks.objects.get(paper=paper,reviewer=reviewer)
			remark.answer = request.POST.get('remarks')
			remark.save()
		else : 
			remark = Remarks()
			remark.paper = paper
			remark.reviewer = reviewer
			remark.answer = request.POST.get('remarks')
			remark.save()

	return redirect('/review/reviewPaper/'+str(paper_id))

def submitReview(request,paper_id):
	reviewer = Reviewer.objects.get(user = request.user)
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	assignObj = AssignedPaperStatus.objects.get(reviewer=reviewer,paper=paper)
	assignObj.reviewStatus = 1
	assignObj.save()

	reviewer.papers.remove(paper)
	reviewer.save()

	return redirect('/review')

def loginReviewer(request):
	if request.user.is_authenticated():
		try:
			user = Reviewer.objects.get(user=request.user)
			if user:
				return HttpResponseRedirect('/review/')
			else:
				return HttpResponseRedirect('/review/404/')
		except:
			return HttpResponseRedirect('/review/404/')
	else:
		response={}
		if request.method == 'POST':
			username=request.POST['username']
			password=request.POST['password']
			user = authenticate(username=username, password=password)
			
			if user is not None:
				login(request, user)
				return HttpResponseRedirect('/review/')
			
			else:
				response['message']='User is invalid'
		return render(request,'reviewer/login.djt',response)

	context = {}
	return render(request, 'reviewer/login.djt', context)

@login_required(login_url='/review/login/')
def logoutReviewer(request):
	logout(request)
	return HttpResponseRedirect('/review/login/')

def err404(request):
	return render(request, 'reviewer/404.djt', {})

def createRev(request) :
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	full_filename = os.path.join(BASE_DIR, 'static/book1.xlsx')
	wb = xlrd.open_workbook(full_filename)
	conference = Conference.objects.get(conference_alias='ctsem2018')
	for s in wb.sheets() :
	    for row in range(1,s.nrows) :
	        mailid = str(s.cell(row,0).value)
	        name = str(s.cell(row,1).value)

	        if mailid=="":
	        	break

	        if User.objects.filter(username=mailid).count() > 0:
	        	continue

	        rev = User()
	        rev.username = mailid
	        rev.email = mailid
	        rev.first_name = name
	        rev.save()

	        rev.set_password("ctsemrev!@#")
	        rev.save()

	        revobj = Reviewer()
	        revobj.user = rev
	        revobj.conference = conference
	        revobj.save()

	return HttpResponse("Rev id's creation done")