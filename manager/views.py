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
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import datetime
import xlwt
import mimetypes
import base64
# from __future__ import print_function
import httplib2
import os
from django.core.mail import EmailMessage
# from mail import main 

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
	try:
		manager = Manager.objects.get(user=request.user)
		conferences = Conference.objects.filter(manager=manager)
		return render(request, 'manager/home.djt', {'conferences':conferences})
	except:
		return redirect('/manager/signin')

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

	manager = Manager.objects.get(user=request.user)
	user = paper.uid
	
	remarks = Paper_Remark.objects.all()
	content = ""

	for rem in remarks:
		if rem.user == user and rem.manager == manager and rem.conf_paper == paper:
			content = rem.content
	print content

	context = {
		'reviewer':reviewer,
		'reviewer_assigned':reviewer_assigned,
		'paper':paper,
		'is_approved':paper.is_approved,
		'is_rejected':paper.is_rejected,
		'under_review':paper.under_review,
		'content':content,
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
	final_papers = []
	rejected_dds = []
	for regconf in regconfs:
		user = regconf.user
		try:
			payment = Payment.objects.get(user=user,conf_id=conference)
			users.append(user)
			paidtrans.append(payment)
		except:
			print "Payment not done"
	paper_conf = Conf_Paper.objects.filter(conf_id=cid)
	for paper in paper_conf:
		papers.append(paper)
		try:
			finalpaper = Final_paper.objects.get(related_paper__paper_id=paper.paper_id)
			final_papers.append(finalpaper)
		except Exception as e:
			print str(e)
			print "No final paper for this yet"

	for pendingtrans in Payment.objects.filter(conf_id=conference):
		if pendingtrans.is_aprooved==False and pendingtrans.is_rejected==False:
			pending_dds.append(pendingtrans)
		if pendingtrans.is_rejected==True:
			rejected_dd = Rejected_payment.objects.filter(conf_id=conference,user=pendingtrans.user)
			for obj in rejected_dd:
				rejected_dds.append(obj)

	response={}
	response['users']=users
	print users
	response['regusercount']=len(users)
	response['paidtrans']=paidtrans
	response['papers']=papers
	response['papercount']=len(papers)
	response['pending_dds']=pending_dds
	response['ddcount']=len(pending_dds)
	response['rejected_dds']=rejected_dds
	response['type']=type
	response['conference']=conference
	response['finalpapers']=final_papers
	response['finalsubcount']=len(final_papers)
	return render(request,'manager/conf_navbar.djt',response)

def reviewerAssigned(request, paper_id, u_id):
	reviewer = Reviewer.objects.get(id=u_id)
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	reviewer.papers.add(paper)
	reviewer.save()
	return HttpResponseRedirect("/manager/assignreviewer/"+paper_id+"/")

def reviewCompleted(request,paper_id,u_id):
	reviewer = Reviewer.objects.get(id=u_id)
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	answers = Answers.objects.filter(reviewer=reviewer).filter(paper=paper)
	ans_len = len(answers)
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
	payment.is_aprooved=True
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
		payment=Payment.objects.get(id=request.POST['payid'])
		payment.remarks=request.POST['remark']
		payment.is_rejected = True
		payment.save()

		now = datetime.datetime.now()
		rejected_payment = Rejected_payment()
		rejected_payment.conf_id = payment.conf_id
		rejected_payment.user = payment.user
		rejected_payment.pic_of_dd = payment.pic_of_dd
		rejected_payment.date = now.strftime("%Y-%m-%d")
		rejected_payment.remarks = payment.remarks
		rejected_payment.save()
		url = '/manager/conference_landing/'+request.POST['cid']+'/2/'
	return redirect(url)


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
	return HttpResponseRedirect('/manager/conference_landing/'+str(paper.conf_id.conference_id)+'/3/')

def isDisapprovedPaper(request, paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	paper.is_approved = False
	paper.is_rejected = True
	paper.under_review = False
	paper.save()
	return HttpResponseRedirect('/manager/conference_landing/'+str(paper.conf_id.conference_id)+'/3/')

def export_xls(request, conference_name):
	queryset = UserProfile.objects.all()
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=UserData.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet("MyModel")

	row_num = 0

	columns = [
	    (u"User", 6000),
	    (u"Gender",6000),
	    (u"Contact",6000),
	    (u"regConferences", 20000),
	]

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	for col_num in xrange(len(columns)):
	    ws.write(row_num, col_num, columns[col_num][0], font_style)
	    ws.col(col_num).width = columns[col_num][1]

	font_style = xlwt.XFStyle()
	font_style.alignment.wrap = 1
	l = len(queryset)

	for query in queryset:
		userp = query

		conf = ""
		reg_con = userp.regConferences.all()
		i=1
		for conferences in reg_con:
			if conferences.conf_id.conference_name == conference_name:
				row_num += 1
				conf += str(i) + ": " + conferences.conf_id.conference_name + " "
				i+=1
				rows = [userp.user.username,userp.gender,userp.contact,conf]
				for col_num in xrange(len(rows)):
					ws.write(row_num, col_num, rows[col_num], font_style)

	wb.save(response)
	return response

def paper_remark(request, paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	manager = Manager.objects.get(user=request.user)
	user = paper.uid
	
	remarks = Paper_Remark.objects.all()
	content = ""

	for rem in remarks:
		if rem.user == user and rem.manager == manager and rem.conf_paper == paper:
			content = rem.content


	if request.method == 'POST':
		content = request.POST['remark']
		remark_check = Paper_Remark.objects.filter(conf_paper=paper).filter(user=user).filter(manager=manager)
		if remark_check:
			remark = remark_check[0]
		else:
			remark = Paper_Remark()
		remark.manager = manager
		remark.user = user
		remark.content = content
		remark.conf_paper = paper

		remark.save() 
		return HttpResponseRedirect('/manager/assignreviewer/' + paper_id +"/")

	return HttpResponseRedirect('/manager/assignreviewer/' + paper_id +"/")


import smtplib
import socks

def sendmail(request):
		
	#socks.setdefaultproxy(TYPE, ADDR, PORT)
	socks.setdefaultproxy(socks.SOCKS5, 'http://172.30.0.22', 3128)
	socks.wrapmodule(smtplib)

	smtpserver = 'smtp.gmail.com'
	AUTHREQUIRED = 1 
	smtpuser = 'kiran.kumar.00796@gmail.com'  
	smtppass = 'lemontrees'  

	RECIPIENTS = 'kiran.kumar.00796@gmail.com'
	SENDER = 'kiran.kumar.00796@gmail.com'
	mssg = "test message"
	s = mssg   

	server = smtplib.SMTP(smtpserver,587)
	server.ehlo()
	server.starttls() 
	server.ehlo()
	server.login(smtpuser,smtppass)
	server.set_debuglevel(1)
	server.sendmail(SENDER, [RECIPIENTS], s)
	server.quit()

# To-Do Email Part
# Cannot import name directory error when executed with python 2.7 but works perfectly for python 3.4

# def create_message_with_attachment(request):

# 	message = MIMEMultipart()
# 	message['to'] = "kiranckonduru@gmail.com"
# 	message['from'] = "kiranckonduru@gmail.com"
# 	message['subject'] = "kiranckonduru@gmail.com"

# 	message_text = "message_text"
# 	msg = MIMEText(message_text)
	
# 	message.attach(msg)

# 	# content_type, encoding = mimetypes.guess_type(file)

# 	# if content_type is None or encoding is not None:
# 	# 	content_type = 'application/octet-stream'
# 	# 	main_type, sub_type = content_type.split('/', 1)
# 	# if main_type == 'text':
# 	# 	fp = open(file, 'rb')
# 	# 	msg = MIMEText(fp.read(), _subtype=sub_type)
# 	# 	fp.close()
# 	# elif main_type == 'image':
# 	# 	fp = open(file, 'rb')
# 	# 	msg = MIMEImage(fp.read(), _subtype=sub_type)
# 	# 	fp.close()
# 	# elif main_type == 'audio':
# 	# 	fp = open(file, 'rb')
# 	# 	msg = MIMEAudio(fp.read(), _subtype=sub_type)
# 	# 	fp.close()
# 	# else:
# 	# 	fp = open(file, 'rb')
# 	# 	msg = MIMEBase(main_type, sub_type)
# 	# 	msg.set_payload(fp.read())
# 	# 	fp.close()
# 	# filename = os.path.basename(file)
# 	# msg.add_header('Content-Disposition', 'attachment', filename=filename)
# 	# message.attach(msg)

# 	return {'raw': base64.urlsafe_b64encode(message.as_string())}

# def send_message(service, user_id, message):
#   """Send an email message.

#   Args:
#     service: Authorized Gmail API service instance.
#     user_id: User's email address. The special value "me"
#     can be used to indicate the authenticated user.
#     message: Message to be sent.

#   Returns:
#     Sent Message.
#   """
#   try:
#     message = (service.users().messages().send(userId=user_id, body=message)
#                .execute())
#     print 'Message Id: %s' % message['id']
#     return message
#   except errors.HttpError, error:
#     print 'An error occurred: %s' % error
