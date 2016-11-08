from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate,login,logout
from .models import Reviewer, Questions, Answers, Remarks
from conference.models import Conf_Paper
from .forms import ReviewForm
import traceback
import sys

# Create your views here.

def checkuserifReviewer(user):
	user = Reviewer.objects.filter(user=user)
	if len(user)>0:
		return True
	else:
		return False


@login_required(login_url='/review/login/')
@user_passes_test(checkuserifReviewer,login_url="/review/404/")
def reviewHome(request):
	user=request.user
	reviewer = Reviewer.objects.get(user = request.user)
	papers = reviewer.papers.all()
	paper = papers
	print paper
	context = {
		"paper" : paper,
	}
	return render(request, 'reviewer/home.djt',context)

@login_required(login_url='/review/login/')
@user_passes_test(checkuserifReviewer,login_url="/review/404/")
def reviewPaper(request, paper_id):
	user = request.user
	reviewer = Reviewer.objects.get(user = request.user)
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	ch_paper = reviewer.papers.filter(paper_id=paper_id)
	if len(ch_paper)<=0:
		raise Http404
	paperpath = str(paper.paperfile)
	conference = paper.conf_id
	questions = Questions.objects.filter(conference=conference)
	form = ReviewForm(request.POST or None)
	q_len = len(questions)
	q_ans = []

	for q in questions:
		try:
			a = Answers.objects.filter(reviewer = reviewer).filter(question = q).filter(paper=paper)
			if len(a)>0:
				q_ans.append(a[0].answer)
			else:
				q_ans.append(1)
		except:
			traceback.print_exc()
	print q_ans

	rem = ""
	try:
		remark = Remarks.objects.filter(reviewer=reviewer).filter(paper=paper)
		if len(remark)>0:
			rem = remark[0].answer
		else:
			rem=""
	except:
		traceback.print_exc()


	if request.method=='POST':
		for q in questions:
			a = Answers.objects.filter(reviewer = reviewer).filter(question = q).filter(paper=paper)
			ans = request.POST['answer'+str(q.id)]
			if a.count() <= 0:
				a = Answers()
				a.question = q
				a.reviewer = reviewer
				a.answer = ans
				a.paper = paper
				a.save()
			else:
				a = Answers.objects.filter(reviewer = reviewer).filter(paper=paper).get(question = q)
				a.answer = ans
				a.save()

		remark = Remarks.objects.filter(reviewer=reviewer).filter(paper=paper)
		if len(remark) > 0:
			re = remark[0]

			re.answer = request.POST['remark']
			re.save()
		else:
			re = Remarks()
			re.answer = request.POST['remark']
			re.paper = paper
			re.reviewer = reviewer
			re.save()
		return HttpResponseRedirect('/review/')

	context = {
		"paperpath":paperpath,
		"paper":paper,
		'rem':rem,
		'questions':questions,
		'form':form,
		'q_len':q_len,
		'q_ans':q_ans,
	}
	return render(request, 'reviewer/singlepaper.djt',context)

def loginReviewer(request):
	if request.user.is_authenticated():
		try:
			user = Reviewer.objects.get(user=request.user)
			if user:
				return HttpResponseRedirect('/review/')
			else:
				return HttpResponseRedirect('/review/404/')
		except:
			print "here"
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




