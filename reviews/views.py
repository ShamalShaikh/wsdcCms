from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Reviewer, Questions, Answers
from conference.models import Conf_Paper
from .forms import ReviewForm
import traceback
import sys

# Create your views here.

@login_required
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

def reviewPaper(request, paper_id):
	user=request.user
	reviewer = Reviewer.objects.get(user = request.user)
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	paperpath = str(paper.paperfile)
	questions = Questions.objects.filter(paper=paper)
	form = ReviewForm(request.POST or None)
	q_len = len(questions)
	q_ans = []

	for i in range(0,10):
		q_ans.append('')

	for q in questions:
		try:
			a = Answers.objects.filter(reviewer = reviewer).get(question = q)
			q_ans.insert(q.id,a.answer)
		except:
			traceback.print_exc()
	print q_ans

	if request.method=='POST':
		for q in questions:
			a = Answers.objects.filter(reviewer = reviewer).filter(question = q)
			ans = request.POST['answer'+str(q.id)]
			if a.count() <= 0:
				a = Answers()
				a.question = q
				a.reviewer = reviewer
				a.answer = ans
				a.save()
			else:
				a = Answers.objects.filter(reviewer = reviewer).get(question = q)
				a.answer = ans
				a.save()
	

	context = {
		"paperpath":paperpath,
		"paper":paper,
		'questions':questions,
		'form':form,
		'q_len':q_len,
		'q_ans':q_ans,
	}
	return render(request, 'reviewer/singlepaper.djt',context)
