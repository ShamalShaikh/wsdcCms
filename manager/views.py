from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from conference.models import Conference, Conf_Paper
from reviews.models import *
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
import datetime

from django.core.mail import send_mail
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
# from mail import main 

def signin(request):
	return render(request,'login_auth/sites/manager_signin.djt')


def signin_auth(request):
	print "signin_auth module"
	response={}
	if request.method=='POST':
		username = request.POST['username']
		try:
			usr = User.objects.get(username=username)
		except:
			usr = None
		manager = Manager.objects.filter(user=usr)
		if request.user.is_authenticated() and manager:
		    return redirect('/manager')
		if request.method == "POST" and manager:
		    password = request.POST['password']
		    user = authenticate(username=username, password=password)
		    if user is not None:
		        login(request, user)
		        return redirect('/manager')
		    else:
		        response['message']='Incorrect Password!'
		if not manager or usr is None:
			response['message']='Only Managers can login!'
		return render(request,'login_auth/sites/manager_signin.djt',response)
	else:
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
	conf_name = paper.conf_id.conference_name
	reviewer = Reviewer.objects.filter(conference=paper.conf_id).exclude(papers=paper)
	reviewer_assigned = Reviewer.objects.filter(papers=paper,conference=paper.conf_id)
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
		'conf_name':conf_name,
	}

	##new part
	revs = AssignedPaperStatus.objects.filter(paper=paper)
	if len(revs) > 0 :
		context['rev1'] = revs[0]
	if len(revs) > 1 :
		context['rev2'] = revs[1]
	if manager == paper.conf_id.manager:
		return render(request, 'manager/assignreviewer.djt', context)
	else:
		return render(request,'manager/404.djt',{})



@login_required(login_url='/manager/signin/')
def conference_landing(request, cid, type):
	# here we need to check whether this conference belongs to this manager or not
	# also we need to check whether this user is manager.
	conference = Conference.objects.get(conference_id=cid)
	manager = Manager.objects.get(user=request.user)
	regconfs = Registered_Conference.objects.filter(conf_id=conference)
	users = []
	paidtrans = []
	pending_dds = []
	papers = []
	final_papers = []
	rejected_dds = []
	unpaid_users = []
	displayPapers = []
	unpaidPapers = []

	for regconf in regconfs:
	    user = regconf.user
	    users.append(UserProfile.objects.get(user=user))
	    paper_conf = Conf_Paper.objects.filter(conf_id=cid, uid=user)

	    if paper_conf.count() > 0:
	        displayPapers.append(paper_conf.first())
	    else:
	        displayPapers.append(None)
	    try:
	        payment = Payment.objects.get(user=user, conf_id=conference)
	    except:
	        unpaid_users.append(UserProfile.objects.get(user=user))
	        unpaidPapers.append(paper_conf.first())
	        print "Payment not done"
	    try:
	        payment = Payment.objects.get(user=user, conf_id=conference, is_aprooved=True)
	        paidtrans.append(payment)
	    except:
	        print "Payment not approved"
	paper_conf = Conf_Paper.objects.filter(conf_id=cid)
	for paper in paper_conf:
	    papers.append(paper)
	    try:
	        finalpaper = Final_paper.objects.get(related_paper__paper_id=paper.paper_id)
	        final_papers.append(finalpaper)
	    except Exception as e:
	        print str(e)
	        print "No final paper for this yet"

	for pendingtrans in Payment.objects.filter(conf_id=cid):
		print 2
		if pendingtrans.is_aprooved==False and pendingtrans.is_rejected==False:
			pending_dds.append(pendingtrans)
			print 1
			# print pendingtrans
		# if pendingtrans.is_rejected==True:
			# rejected_dd = Rejected_payment.objects.filter(conf_id=cid,user=pendingtrans.user)
			# for obj in rejected_dd:
			# 	rejected_dds.append(obj)

	contestants = Contest.objects.all()

	print Payment.objects.filter(conf_id=cid).count()
	registered_payments = AccomodationPayment.objects.filter(is_rejected=False,is_aprooved=False)
	approved_accomodtions = AccomodationPayment.objects.filter(is_aprooved=True)
	response = {}
	response["reg_pays"] = registered_payments
	response["app_accomo"] = approved_accomodtions
	response["app_accomo_count"] = approved_accomodtions.count()
	response["accomo_count"] = registered_payments.count()
	response['users'] = users
	response['regusercount'] = len(users)
	response['paidtrans'] = paidtrans
	response['paidusers'] = len(paidtrans)
	response['unpaid_users'] = unpaid_users
	response['unpaidUsersPapers'] = zip(unpaid_users, unpaidPapers)

	response['papers'] = papers
	response['papercount'] = len(papers)
	response['pending_dds'] = pending_dds
	response['ddcount'] = len(pending_dds)
	response['rejected_dds'] = rejected_dds
	response['type'] = type
	response['conference'] = conference
	response['finalpapers'] = final_papers
	response['finalsubcount'] = len(final_papers)
	response['contestants'] = contestants
	response['contestantCount'] = len(contestants)
	response['displayUsers'] = zip(users, displayPapers)

	print manager
	if manager == conference.manager:
	    return render(request, 'manager/conf_navbar.djt', response)
	else:
	    return render(request, 'manager/404.djt', {})

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
			sum = sum+int(i.marks)
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
	try:
		regconf = Registered_Conference.objects.get(conf_id=payment.conf_id,user=payment.user)
	except:
		regconf = Registered_Conference()
		regconf.user = payment.user
		regconf.conf_id = payment.conf_id
		regconf.save()
	#print regconf.conf_id.conference_id
	print request.POST
	sendmail(request,str(regconf.conf_id.conference_id),'2')
	return redirect('/manager/conference_landing/' + str(regconf.conf_id.conference_id) + "/" + '2' + "/")

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
		rejected_payment.refno = payment.regno
		rejected_payment.date = now.strftime("%Y-%m-%d")
		rejected_payment.remarks = payment.remarks
		rejected_payment.save()
		print request.POST
		sendmail(request,request.POST['cid'],'2')
		return redirect('/manager/conference_landing/' + request.POST['cid'] + "/" + '2' + "/")


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


def isApprovedPaper(request, type,paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	paper.is_approved = True
	paper.is_rejected = False
	paper.under_review = False
	paper.status = int(type)+1
	paper.save()
	# for inceee2019 conference
	# status = 2 means for oral presentation
	# status = 3 means for poster presentation
	alias = paper.conf_id.alias
	print("Paper status: "+ str(paper.status))
	if paper.status == 2 or paper.status == 3 :
		sendMailFunction(paper.uid.email,paper.papername,paper.paperRefNum,paper.status,alias)

	return HttpResponseRedirect('/manager/conference_landing/'+str(paper.conf_id.conference_id)+'/3/')

def isDisapprovedPaper(request, paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	paper.is_approved = False
	paper.is_rejected = True
	paper.under_review = False
	paper.status = 4
	paper.save()
	sendMailFunction(paper.uid.email,paper.papername,paper.paperRefNum,paper.status,paper.conf_id.alias)
	return HttpResponseRedirect('/manager/conference_landing/'+str(paper.conf_id.conference_id)+'/3/')


def export_xls(request, cid):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=UserData.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet("Papers' Data")

	row_num = 0

	# columns = [
	# 	(u"Reference Number",6000),
	#     (u"User", 6000),
	#     (u"Gender",6000),
	#     (u"Contact",6000),
	#     (u"Email",6000),
	#     (u"Institute",10000),
	#     (u"Department",6000),
	#     (u"Tile Of Paper",20000),
	#     (u"TimeStamp",6000),
	#     (u"Conference", 20000),
	#     (u"Reviewer 1",6000),
	#     (u"Reviewer 2",6000),
	#     (u"Average",6000),
	# ]

	columns = [
	    (u"Registered Users", 6000),
		(u"Paper Name",10000),
		(u"Paper Ref No.",6000),
		(u"Paper Type",6000),
	    (u"Gender",3000),
	    (u"Contact",6000),
	    (u"Email",6000),
	    (u"Institute",10000),
	    (u"Department",6000),
	    (u"Conference", 9000),
		(u"Payment Status", 6000),
		(u"Payment Ref No.", 9000),
	]

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	for col_num in xrange(len(columns)):
	    ws.write(row_num, col_num, columns[col_num][0], font_style)
	    ws.col(col_num).width = columns[col_num][1]
	row_num += 1

	font_style = xlwt.XFStyle()
	font_style.alignment.wrap = 1

	conference = Conference.objects.get(conference_id=cid)
	# papers = Conf_Paper.objects.filter(conf_id=conference)
	reg_confs = Registered_Conference.objects.filter(conf_id=cid)
	# totalRows = len(papers)
	totalRows = len(reg_confs)

	# for paper in papers:

	# 	row_num += 1

	# 	refnum = str(paper.paperRefNum)
	# 	nameOfPerson = paper.uid.first_name + " " + paper.uid.last_name
	# 	gender = paper.uid.profile.gender
	# 	contact = paper.uid.profile.contact
	# 	email = paper.uid.email
	# 	institute = paper.uid.profile.institute
	# 	department = paper.uid.profile.department
	# 	title = paper.papername
	# 	localTime =  paper.submissionDate+datetime.timedelta(hours=5,minutes=30)
	# 	timestamp = str(localTime.strftime('%d-%m-%Y %I:%M %p'))
	# 	confname = conference.conference_name

	# 	dataRow = [refnum, nameOfPerson, gender, contact, email, institute, department,
	# 				title, timestamp, confname ,"-","-","-"]

	# 	index = 10
	# 	finalavg = 0.0
	# 	assignPaperObj = AssignedPaperStatus.objects.filter(paper=paper)
	# 	for obj in assignPaperObj :
	# 		answers = Answers.objects.filter(paper=paper,reviewer=obj.reviewer)
	# 		avg = 0.0
	# 		count = 0
	# 		for answer in answers :
	# 			if answer.question.que_type == 0 :
	# 				count += 1
	# 				avg += answer.marks
	# 		rev = avg/count
	# 		finalavg += rev
	# 		dataRow[index] = str(rev)
	# 		index += 1

	# 	if index==12:
	# 		finalavg = (finalavg/2)
	# 	dataRow[12] = str(finalavg)

	# 	for col_num in xrange(len(dataRow)) :
	# 		ws.write(row_num, col_num, dataRow[col_num], font_style)

	# wb.save(response)

	for reg_conf in reg_confs:

		# row_num += 1

		# refnum = str(paper.paperRefNum)
		papers = Conf_Paper.objects.filter(conf_id=cid,uid=reg_conf.user)
		nameOfPerson = reg_conf.user.first_name + " " + reg_conf.user.last_name
		paperName = "NA"
		paperRefNo = "NA"
		paperStatus = -1
		paperType = "NA"
		multiple_paper = [[0 for x in range(3)] for y in range(len(papers))]
		i=0
		if papers.exists() :
			for paper in papers :  
				paperName = paper.papername
				paperRefNo = paper.paperRefNum
				paperStatus = paper.status
				paperType = ""
				if paperStatus == 0 :
					paperType = "Under Review"
				if paperStatus == 1 :
					paperType = "Asked for Revision"
				if paperStatus == 2 :
					paperType = "Oral Presentation"
				if paperStatus == 3 :
					paperType = "Poster Presentation"
				if paperStatus == 4 :
					paperType = "Rejected"
				
				multiple_paper[i] = [paperName, paperRefNo, paperType]
				i=i+1
		
		gender = reg_conf.user.profile.gender
		contact = reg_conf.user.profile.contact
		email = reg_conf.user.email
		institute = reg_conf.user.profile.institute
		department = reg_conf.user.profile.department
		# title = paper.papername
		# localTime =  paper.submissionDate+datetime.timedelta(hours=5,minutes=30)
		# timestamp = str(localTime.strftime('%d-%m-%Y %I:%M %p'))
		confname = conference.conference_name
		payment = ""
		refno = ''

		#showing only first payment of the user
		if Payment.objects.filter(conf_id=cid,user=reg_conf.user).exists():
			user = Payment.objects.all().filter(conf_id=cid,user=reg_conf.user)
			if user[0].is_aprooved==True:
				payment= "PAYMENT VERIFIED"
				refno = user[0].refno
			if user[0].is_aprooved==False and user[0].is_rejected==False:
				payment = "VERIFICATION PENDING"
				refno = user[0].refno
			if user[0].is_rejected==True:
				payment = "PAYMENT REJECTED"
				refno = user[0].refno
		
		else:
			payment = "NOT PAID"
			refno = "NA"



		# if reg_conf.user.profile.mail_sent_register:
		# 	payment = "NOT PAID"
		# if reg_conf.user.profile.mail_sent_reject:
		# 	payment = "PAYMENT REJECTED"
		# if reg_conf.user.profile.mail_sent_accept:
		# 	payment = "PAYMENT ACCEPTED"

		# dataRow = [nameOfPerson, paperName, paperRefNo, paperType, gender, contact, email, institute, department,
		# 			confname, payment,refno]

		# index = 8
		# finalavg = 0.0
		# assignPaperObj = AssignedPaperStatus.objects.filter(paper=paper)
		# for obj in assignPaperObj :
		# 	answers = Answers.objects.filter(paper=paper,reviewer=obj.reviewer)
		# 	avg = 0.0
		# 	count = 0
		# 	for answer in answers :
		# 		if answer.question.que_type == 0 :
		# 			count += 1
		# 			avg += answer.marks
		# 	rev = avg/count
		# 	finalavg += rev
		# 	dataRow[index] = str(rev)
		# 	index += 1

		# if index==12:
		# 	finalavg = (finalavg/2)
		# dataRow[12] = str(finalavg)

		if multiple_paper : 
			for paper in multiple_paper : 
				dataRow = [nameOfPerson, paper[0], paper[1], paper[2], gender, contact, email, institute, department,
							confname, payment,refno]
				for col_num in xrange(len(columns)) :
					ws.write(row_num, col_num, dataRow[col_num], font_style)
				row_num += 1
		else :
			dataRow = [nameOfPerson, paperName, paperRefNo, paperType, gender, contact, email, institute, department,
							confname, payment,refno]
			for col_num in xrange(len(columns)) :
					ws.write(row_num, col_num, dataRow[col_num], font_style)
			row_num +=1

	wb.save(response)
	return response

def paper_remark(request, paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	manager = Manager.objects.get(user=request.user)
	user = paper.uid

	if request.method == 'POST':
		remark_check = Paper_Remark.objects.filter(conf_paper=paper,manager=manager,user=user)
		if remark_check:
			remark = remark_check[0]
		else:
			remark = Paper_Remark()
		remark.manager = manager
		remark.user = user
		remark.remarkFile = request.FILES['remarkFile']
		remark.content = ''
		remark.conf_paper = paper
		remark.save()

		paper.status = 1
		paper.save()

		return redirect('/manager/assignreviewer/' + paper_id +"/")

	return redirect('/manager/assignreviewer/' + paper_id +"/")

def sendmail(request,cid,type):
    profile = UserProfile.objects.get(pk=request.POST['user'])
    conference = Conference.objects.get(pk=cid)
    receiver = profile.user.email
    print "HELLLO....."+request.POST['user'] + receiver
    sender = 'conference@nitw.ac.in'
    mail_Action = request.POST.get('mail_action',0)
    subject = ''
    content = ''
    print sender
    print type
    if type == '1':
        subject = 'Application approved but payment pending'
        content = "Dear " + profile.user.first_name + ",\n\n"
        content += "Your details have been reviewed and verified by us, and paper is accepted for presentation\n\n"
        content += "Please pay the registration fee to proceed further.\n\n"
        content += "Thank you!"

    if type == '2':
        if mail_Action == "approve":
            subject = 'Payment verified.Invitation to Conference ' + conference.conference_name
            content = "Dear " + profile.user.first_name + ",\n\n"
            content += "Your payement has been successfully verified.\n\n"
            # content += "You are invited to the Conference on 10th October.\n\n"
            content += "Time Table for the conference will be uploaded in the website shortly.\n\n"
            content += "Thank you!"

        else:
            subject = 'Payment verification Failed'
            content = "Dear " + profile.user.first_name + ",\n\n"
            content += "There was an issue in verifying your payment for the conference: " + conference.conference_name + "\n"
            content += "Issue: " + request.POST['remark'] + "\n\n"
            content += "Please send the payment details again."

    if type == '5':
        subject = 'Payment verified.Invitation to Conference ' + conference.conference_name
        content = "Dear " + profile.user.first_name + ",\n\n"
        content += "Your payement has been successfully verified.\n\n"
        # content += "You are invited to the Conference on 10th October.\n\n"
        content += "Time Table for the conference will be uploaded in the website shortly.\n\n"
        content += "Thank you!"

    rlist = []
    rlist.append(receiver)
    print subject
    print content
    print rlist
    try:
        # send_mail(subject,content,sender,rlist,fail_silently=False)
        mail = EmailMultiAlternatives(subject, content, sender, rlist)
        mail.send()
        print "tpe:"+type
        if type == '1':
            profile.mail_sent_register=True

        if type == '2' and mail_Action == "approve":
            profile.mail_sent_reject=False
            profile.mail_sent_accept=True
            print "type:"+type
        if type == '2' and mail_Action == "disapprove":
            profile.mail_sent_reject=True
            profile.mail_sent_accept=False
            print "type:"+type

        if type == '5':
            profile.mail_sent_accept=True
            print "type:"+type
        profile.save()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

    return redirect('/manager/conference_landing/' + cid + "/" + type + "/")



def sendMailFunction(email,papername,trackingID,presentation_type,alias) : 
	# if alias == 'mmse2018' :
	# 	receiver = email
	# 	sender = 'mmse2018.nitw@gmail.com'
		
	# 	####
	# 	content = "Dear Author<br><br>"
	# 	content += "Your manuscript was peer reviewed for presentation and publication "
	# 	content += "in the Proceedings/journal "
	# 	content += "of the National Conference on "
	# 	content += "FRONTIERS IN CORROSION CONTROL OF MATERIALS (FCCM-2018) "
	# 	content += "to be held on June 28-29, 2018 at Department of Metallurgical and Materials Engineering "
	# 	content += "National Institute of Technology, Warangal, Telangana, India.<br><br>"
	# 	content += "Based on the evaluations of reviewers, it is my pleasure to "
	# 	content += "inform that your revised paper entitled "
	# 	content += '" ' + papername + ' " (' + trackingID + ") "
	# 	content += "has been accepted for "
	# 	content += "presentation and will be scheduled in an appropriate session.<br><br>"
	# 	content += "This letter hereby serves the purpose of your official letter of "
	# 	content += "invite to the FCCM-2018 conference.<br><br>"
	# 	content += "It is to be noted that at least one author of each paper should "
	# 	content += "be registered for the conference by paying the appropriate "
	# 	content += "registration fee as well as everybody attending the conference.<br><br>"
	# 	content += "Further, You are required to pay the registration fee "
	# 	content += "upload the final version of the paper along "
	# 	content += "with the payment receipt on the conference website.<br><br>"
	# 	content += "We are looking forward welcoming you in the Conference.<br><br>"
	# 	content += "Sincerely yours,<br>"

	# 	content += '<br> <img src="cid:sign.png"> <br>'
	# 	content += "(D. SRINIVASACHARYA)<br><br>"
	# 	content += "Conference Chair<br><br>"
	# 	content += "Instructions for uploading the Final Submission and Payment "
	# 	content += "of Registration fee : <br><br>"
	# 	content += "\t 1. Upon acceptance of a manuscript for publication/presentation, "
	# 	content += "the author has to pay the full registration fee.<br>"
	# 	content += "\t 2. The payment of the registration fee is through NEFT (or in worst case DD)."
	# 	content += "The detials of online payment are given on the conference website.<br>"
	# 	content += '\t 3. Select "upload payment Receipt" (Scanned copy of the '
	# 	content += "online payment receipt or DD) option from the navbar at top.<br>"
	# 	content += "\t 4. Upload picture of ID proof and the payment receipt.<br>"
	# 	content += '\t 5. Then from the same upload paper option, go to "final paper upload".<br>'
	# 	content += "\t 6. Upload Copyright Form (which is available at important links page).<br>"
	# 	content += "\t 7. Upload final paper, and you are done !!!<br><br>"
	# 	content += '\n\nIn case of any queries mail to mmse2018.nitw@gmail.com .\n\n'

	# 	rlist = []
	# 	rlist.append(receiver)

	# 	msg = EmailMultiAlternatives('Acceptance of Paper for Publication in MMSE-2018',content,sender,rlist)

	# 	msg.attach_alternative(content, "text/html")

	# 	msg.mixed_subtype = 'related'

	# 	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	# 	fp = open(os.path.join(BASE_DIR, 'static/sign.png'), 'rb')
	# 	msg_img = MIMEImage(fp.read())
	# 	fp.close()
	# 	msg_img.add_header('Content-ID', '<{}>'.format('sign.png'))
	# 	msg.attach(msg_img)

	# 	try:
	# 		msg.send()
	# 		# send_mail('Acceptance of Paper for Publication',content,sender,rlist,fail_silently=False,)
	# 	except BadHeaderError:
	# 		return HttpResponse('Invalid header found.')

	if alias == 'fccm2018' :
		receiver = email
		sender = 'fccm2018nitw@gmail.com'
		
		####
		content = "Dear Author\n\n"
		content += "Your abstract was peer reviewed for presentation "
		content += "at the National Conference on "
		content += "FRONTIERS IN CORROSION CONTROL OF MATERIALS (FCCM-2018) "
		content += "to be held on June 28-29, 2018 at Department of Metallurgical and Materials Engineering "
		content += "National Institute of Technology, Warangal, Telangana, India.\n\n"
		content += "Based on the evaluations of reviewers, it is my pleasure to "
		content += "inform that your full paper entitled "
		content += '" ' + papername + ' " (' + trackingID + ") "
		content += "has been accepted for "
		content += "presentation and will be scheduled in an appropriate session.\n\n"
		content += "This letter hereby serves the purpose of your official letter of "
		content += "invite to the FCCM-2018 conference.\n\n"
		content += "The selected papers from the papers presented at FCCM conference will be published in "
		content += "Elsevier's journal entitled Materials Today: Proceedings (Journal) "
		content += "after a thorough peer-review process. "
		content += "Hence, authors are requested to submit original research work of high quality and standards. "
		content += "Upon the notification of acceptance for publication in the journal Materials Today: Proceedings (Journal), "
		content += "the authors will have to submit copyright transfer agreement.\n\n"
		content += "It is to be noted that at least one author of each paper should "
		content += "be registered for the conference by paying the appropriate "
		content += "registration fee as well as everybody attending the conference.\n\n"
		content += "Further, You are required to pay the registration fee and "
		content += "upload the final version of the paper along "
		content += "with the payment receipt on the conference website.\n\n"
		content += "We are looking forward welcoming you in the Conference.\n\n"
		content += "Sincerely yours,\n"

		rlist = []
		rlist.append(receiver)

		try:
			send_mail('Acceptance of Paper for Presentation in FCCM-2018',content,sender,rlist,fail_silently=False,)
		except BadHeaderError:
			return HttpResponse('Invalid header found.')

	if alias == 'inceee2019' :
		receiver = email
		sender = 'inceee2019@gmail.com'
		subject = ''
		content = "Dear Author,\n\n"
		content += "Paper: " + trackingID + "\n"
		content += "Title: " + papername + "\n\n"
		if presentation_type == 2 :
			subject = 'Acceptance of Paper for Oral Presentation in INCEEE-2019'
			content += "We are happy to inform you that your abstract of the above-mentioned paper has been accepted "
			content += "for oral presentation at INCEEE2019. You are requested to confirm your registration by uploading\n\n"
			content += "(i) full paper and copyright form as per the template (available at http://cms.nitw.ac.in/conference/inceee2019/links/) "
			content += "in the upload paper tab of the website.\n"
			content += "(ii) the proof of payment after paying registration fee (details at http://cms.nitw.ac.in/inceee2019#fee_div) and\n"
			content += "(iii) filled-in registration form in the Payment Section of the Website.\n\n" 
		if presentation_type == 3 :
			subject = 'Acceptance of Paper for Poster Presentation in INCEEE-2019'
			content += "We are happy to inform you that your abstract of the above-mentioned paper has been accepted "
			content += "for poster presentation at INCEEE2019. You are requested to confirm your registration by uploading\n\n"
			content += "(i) the proof of payment after paying registration fee (details at http://cms.nitw.ac.in/inceee2019#fee_div) and\n"
			content += "(ii) filled-in registration form in the Payment Section of the Website.\n\n"
			content += "Poster size: A0 (841 x 1189 mm, 33.1 x 46.8 in)\n\n"
		if presentation_type == 4 :
			subject = 'Non-Acceptance of Paper for Presentation in INCEEE-2019'
			content += "We regret to inform you that your abstract of the above-mentioned paper has not been accepted "
			content += "for presentation at INCEEE2019. However, you are welcome to participate (as nonpresenting author) by uploading \n\n"
			content += "(i) the proof of payment after paying registration fee (details at http://cms.nitw.ac.in/inceee2019#fee_div) and\n"
			content += "(ii) filled-in registration form in the Payment Section of the Website.\n\n\n"
		content += "Thank you for considering INCEEE-2019 for presenting your research. We look forward to your participation at INCEEE-2019.\n\n"
		content += "Please do not reply to this mail.For any query mail at inceee2019@gmail.com\n\n"
		content += "Coordinators \nINCEEE2019"

		rlist = []
		rlist.append(receiver)
		cc_list = []
		cc_list.append(sender)

		try:
			mail = EmailMultiAlternatives(subject, content, sender, rlist, cc=cc_list)
			mail.send()
		except BadHeaderError:
			return HttpResponse('Invalid header found.')

	return


##Reviewer Assigment part
@login_required(login_url='/manager/signin/')
def assignToReview(request,paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	alias = paper.conf_id.alias
	if request.method == 'POST' :
		username = request.POST.get('username')
		reviewer = Reviewer.objects.get(user__username=username)

		assignPaperObj = AssignedPaperStatus()
		assignPaperObj.paper = paper
		assignPaperObj.reviewStatus = 0
		assignPaperObj.reviewer = reviewer
		assignPaperObj.save()

		reviewer.papers.add(paper)
		reviewer.save()

		sendAssignmentMail(reviewer.user.email,paper,"assigned")

		ques = Questions.objects.filter(conference=paper.conf_id)
		for que in ques:
			if Answers.objects.filter(question=que,paper=paper,reviewer=reviewer).count() == 0 :
				ansobj = Answers()
				ansobj.question = que
				ansobj.answer = ""
				ansobj.reviewer = reviewer
				ansobj.paper = paper
				ansobj.save()

	return redirect('/manager/assignreviewer/'+paper_id)

@login_required(login_url='/manager/signin/')
def reviewDetails(request,revid):
	response = {}
	assignPaperObj = AssignedPaperStatus.objects.get(id=revid)
	response['reviewDetails'] = assignPaperObj
	paper = assignPaperObj.paper
	reviewer = assignPaperObj.reviewer

	ques = Questions.objects.filter(conference=paper.conf_id)
	for que in ques:
		if Answers.objects.filter(question=que,paper=paper,reviewer=reviewer).count() == 0 :
			ansobj = Answers()
			ansobj.question = que
			ansobj.answer = ""
			ansobj.reviewer = reviewer
			ansobj.paper = paper
			ansobj.save()

	answers = Answers.objects.filter(paper=assignPaperObj.paper,reviewer=assignPaperObj.reviewer)
	response['answers'] = answers

	avg = 0.0
	count = 0
	for answer in answers :
		if answer.question.que_type == 0 :
			count += 1
			avg += answer.marks
	response['avg'] = avg/count

	if Remarks.objects.filter(paper=paper,reviewer=reviewer).count() > 0:
		response['remark'] = Remarks.objects.get(paper=paper,reviewer=reviewer)

	return render(request,'manager/reviewresp.djt',response)

@login_required(login_url='/manager/signin/')
def reassign(request,revid):
	assignPaperObj = AssignedPaperStatus.objects.get(id=revid)
	assignPaperObj.reviewStatus = 0
	assignPaperObj.save()

	assignPaperObj.reviewer.papers.add(assignPaperObj.paper)

	sendAssignmentMail(assignPaperObj.reviewer.user.email,assignPaperObj.paper,"reassigned")

	return redirect('/manager/reviewDetails/'+revid)


def sendAssignmentMail(email,paper,act):
	receiver = email
	sender = 'inceee2019@gmail.com'

	content = 'Dear Reviewer,\n\n'
	content += 'Paper : '+paper.papername+' \n\nReference number : '+paper.paperRefNum
	content += '\n\n has been '+act+' to you for review by conference manager of '
	content += paper.conf_id.conference_name+'\n\n'
	content += 'Kindly go to the following link and review the paper on '
	# content += 'or before April 7, 2018 : \n\n'
	content += 'http://cms.nitw.ac.in/review \n\n'
	content += 'Your username is : '+email+'\nYour password is : ctsemrev!@#\n\n'
	content += 'Thanking You\nRegards\nOrganizing Committee\nINCEEE2019\n\n'

	rlist = []
	rlist.append(receiver)

	try:
		send_mail('Review Paper for '+paper.conf_id.conference_name,content,sender,rlist,fail_silently=False,)
	except BadHeaderError:
		return HttpResponse('Invalid header found.')

	return

def approveaccomo(request):
	if request.method == "POST":
		Name = request.POST["Name"]
		type = request.POST["type"]
		house_choice = request.POST["house"]
		slip = request.POST["slip"]
		house_choice = Accomodation.objects.get(houseName=house_choice)
		payment = AccomodationPayment.objects.get(Name=Name, house_choice=house_choice, payment_receipt=slip)
		if type == "approve":
			payment.house_choice.seatsAvailable-=1
			payment.house_choice.save()
			payment.is_aprooved = True
			payment.review = "Approved!"
		if type == "reject":
			payment.review = request.POST["review"]
			payment.is_rejected = True
		email = payment.email
		review = payment.review
		start = str(payment.start_date)
		end = str(payment.end_date)
		payment.save()
		send_accomodation_mail(email,type,review, payment.house_choice.houseName,start,end)
	return redirect('/manager/conference_landing/13/7/')

def send_accomodation_mail(email, type, review,house,start,end):
	reciever = email
	sender = 'conference@nitw.ac.in'
	content = ""
	if type == "approve":
		content += "Congrats you have been alloted " + house + "\n"
		content += "You can be in room from "+start + " to " + end
	if type == "reject":
		content += "Your Request is rejected for House: "+house+"\n"
		content +="For the Reason" + review+"\n"
	content += "Thank you for considering INCEEE-2019 for presenting your research. We look forward to your participation at INCEEE-2019.\n\n"
	content += "Please do not reply to this mail.For any query mail at inceee2019@gmail.com\n\n"
	content += "Coordinators \nINCEEE2019"
	rlist = []
	rlist.append(reciever)

	try:
		send_mail('Accomodation INCEEE2019',content,sender,rlist,fail_silently=False,)
	except BadHeaderError:
		return HttpResponse('Invalid header found.')


def accomodationData(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=AccomodationData.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet("Papers' Data")

	row_num = 0

	columns = [
	    (u"Name", 6000),
		(u"Paper Ref No.",6000),
		(u"Payment Status", 6000),
		(u"Payment Ref No.", 9000),
		(u"Alloted House",9000)
	]

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	for col_num in xrange(len(columns)):
	    ws.write(row_num, col_num, columns[col_num][0], font_style)
	    ws.col(col_num).width = columns[col_num][1]
	row_num += 1

	font_style = xlwt.XFStyle()
	font_style.alignment.wrap = 1

	accomo_pay = AccomodationPayment.objects.all()
	for accomo in accomo_pay:
		nameOfPerson = accomo.Name
		paperRefNo = accomo.paper_id
		payment_status = ""
		if accomo.is_aprooved :
			payment_status = "Approved"
		elif accomo.is_rejected :
			payment_status = "Rejected"
		else:
			payment_status = "In Review"
		paymentRefNo = accomo.reference_number
		alloted_house = accomo.house_choice.houseName
		dataRow = [nameOfPerson,paperRefNo,payment_status,paymentRefNo,alloted_house]
		for col_num in xrange(len(columns)) :
				ws.write(row_num, col_num, dataRow[col_num], font_style)
		row_num +=1
	wb.save(response)
	return response

###################

def contestantList(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=ContestantsList.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet("List")

	row_num = 0

	columns = [
		(u"Name",6000),
	    (u"Category",6000),
	]

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	for col_num in xrange(len(columns)):
	    ws.write(row_num, col_num, columns[col_num][0], font_style)
	    ws.col(col_num).width = columns[col_num][1]

	font_style = xlwt.XFStyle()
	font_style.alignment.wrap = 1

	contestants = Contest.objects.all()
	totalRows = len(contestants)

	for con in contestants:

		row_num += 1

		nameOfPerson = con.contestant.first_name + ' ' + con.contestant.last_name
		category = con.category

		dataRow = [nameOfPerson, category]

		for col_num in xrange(len(dataRow)) :
			ws.write(row_num, col_num, dataRow[col_num], font_style)

	wb.save(response)
	return response
