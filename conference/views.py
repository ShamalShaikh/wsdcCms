from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse,HttpResponseForbidden
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from conference.models import *
from login_auth.models import *
from manager.models import *
import datetime
from sendfile import sendfile
from random import randint
from django.core.mail import send_mail
import smtplib
import os

# Create your views here.
@login_required(login_url='/signin/mmse2018')
def paperdownload(request, paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	if not request.user.is_superuser and request.user != paper.uid:
		return HttpResponseForbidden('Sorry, you cannot access this file')
	return sendfile(request, paper.paperfile.path)

@login_required(login_url='/signin/mmse2018')
def remarkdownload(request, paper_id):
	paper = Conf_Paper.objects.get(paper_id=paper_id)
	remark = Paper_Remark.objects.get(conf_paper=paper)
	if not request.user.is_superuser and request.user != paper.uid:
		return HttpResponseForbidden('Sorry, you cannot access this file')
	return sendfile(request, remark.remarkFile.path)

@login_required(login_url='/signin/mmse2018')
def finalpaperdownload(request, final_paper_id):
	paper = Final_paper.objects.get(id=final_paper_id)
	if not request.user.is_superuser and request.user != paper.related_paper.uid:
		return HttpResponseForbidden('Sorry, you cannot access this file')
	return sendfile(request, paper.final_file.path)

@login_required(login_url='/signin/mmse2018')
def finalcfdownload(request, final_paper_id):
	paper = Final_paper.objects.get(id=final_paper_id)
	if not request.user.is_superuser and request.user != paper.related_paper.uid:
		return HttpResponseForbidden('Sorry, you cannot access this file')
	return sendfile(request, paper.copyright_form.path)

def validateFormat(filename):
    ext = os.path.splitext(filename.name)[1]
    valid_extentions = ['.pdf','.PDF','.docx','.docs','.doc']
    if not ext in valid_extentions:
        return False
    return True

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

@login_required(login_url='/signin/mmse2018')
def make_payment(request,alias):
	conference = Conference.objects.get(conference_alias=alias)
	payments = Payment.objects.filter(user=request.user,conf_id=conference)
	rejected_payments = Rejected_payment.objects.filter(user=request.user,conf_id=conference)
	response = {}
	response['conference'] = conference
	response['payments'] = payments
	response['rejected_payments'] = rejected_payments
	return render(request,'conference/payment.djt',response)

@login_required(login_url='/signin/mmse2018')
def payment(request,alias):
	if request.method == 'POST' :
		# validation
		dd_pic = request.FILES['dd_file']
		id_pic = request.FILES.get('id_file','')
		refno = request.POST['refno']
		user = request.user
		conf_id = Conference.objects.get(conference_alias=alias)
		amount = 0
		now = datetime.datetime.now()

		previousPayment = Payment.objects.filter(user=request.user,conf_id=conf_id)
		print previousPayment
		#This was overwriting the previous payment of the user
		# if len(previousPayment)==1:
		# 	previousPayment[0].pic_of_dd = dd_pic
		# 	previousPayment[0].pic_of_id = id_pic
		# 	previousPayment[0].refno = refno
		# 	previousPayment[0].is_rejected = False
		# 	previousPayment[0].remarks = ""
		# 	previousPayment[0].date = now.strftime("%Y-%m-%d")
		# 	previousPayment[0].save()
		# else:
		pay = Payment()
		pay.amount = amount
		pay.user = user
		pay.conf_id = conf_id
		pay.pic_of_dd = dd_pic
		pay.pic_of_id = id_pic
		pay.refno = refno
		pay.is_approved = False
		pay.payment_mode = 'dd'
		pay.date = now.strftime("%Y-%m-%d")
		pay.save()
		url = '/conference/'+alias
		return redirect(url)
	return render(request,'conference/payment.djt',{'conference':conference})

@login_required(login_url='/signin/mmse2018')
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
			if not validateFormat(paper.paperfile) :
				return HttpResponse('Only Pdf format is allowed')
			# paper.submissionDate=now.strftime("%Y-%m-%d")
			paper.submissionDate = now
			paper.status = 0
			conference.paperCount += 1
			conference.save()
			tempRefnum = ''
			if alias == 'inceee2019':
				timeRef = str(now.year)[2]+str(now.year)[3]+str(now.month).zfill(2)+str(now.day).zfill(2)
				count = 1
				tempRefnum = timeRef + str(count).zfill(2)
				while Conf_Paper.objects.filter(paperRefNum=tempRefnum).count() > 0:
					count += 1
					tempRefnum = timeRef + str(count).zfill(2)
			else:
				count = 30
				tempRefnum = '18'+str(randint(1000, 9999))
				if Conf_Paper.objects.filter(paperRefNum=tempRefnum).count() > 0 :
					print "existing refnum"
					while count > 0:
						tempRefnum = '18'+str(randint(1000, 9999))
						if Conf_Paper.objects.filter(paperRefNum=tempRefnum).count() > 0 :
							count -= 1
							continue
						else:
							break
				if count==0:
					count = 1
					tempRefnum = '18' + str(count).zfill(4)
					while Conf_Paper.objects.filter(paperRefNum=temprefnum).count() > 0 :
						count += 1
						tempRefnum = '18' + str(count).zfill(4)
			
			paper.paperRefNum = tempRefnum
			paper.save()
			regconf.papers.add(paper)
			regconf.save()

			sendTrackingMail(paper,alias)

	url = '/conference/'+conference.conference_alias+"/dashboard/"
	return redirect(url)

@login_required(login_url='/signin/mmse2018')
def dashboard(request,alias):
	now = datetime.datetime.now()
	response = {}
	response['alias']=alias
	conference = Conference.objects.filter(conference_alias=alias)[0]
	conferences = Registered_Conference.objects.filter(user=request.user)
	payments = Payment.objects.filter(user=request.user)
	response['conference']= conference
	response['conferences'] = conferences
	response['payments'] = payments
	print(conference)
	print(payments)
	try:
		receipt = Payment.objects.get(user=request.user,conf_id=conference)
		if receipt.is_aprooved :
			response['receipt'] = True
		else :
			response['receipt'] = False
		print(receipt)
	except:
		response['receipt'] = False
	papers = {}
	finalpapers =[]
	try :
		papers = Conf_Paper.objects.filter(uid=request.user, conf_id=conference)
	except Exception as e:
		print str(e)
		papers = {}
	if len(papers) < conference.max_papers:
		response['upload_paper'] = True
	else:
		response['upload_paper']=False 
	response['papers']=papers
	for paper in papers:
		# print paper.paper_id
		try:
			finalpaper = Final_paper.objects.get(related_paper__paper_id=paper.paper_id)
			finalpapers.append(finalpaper)
		except Exception as e:
			print str(e)
			print "No final paper for this yet"

	print finalpapers
	response['finalpapers'] = finalpapers
			
	if len(finalpapers) < conference.max_papers:
		response['final_paper'] = True
	else:
		response['final_paper'] = False

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

	if alias == 'ctsem2018' :
		response['receipt'] = True
	return render(request, 'conference/upload_paper.djt',response)

def treat(request):
	conference = Conference.objects.get(conference_alias='treat17')
	response = {}
	response['conference']=conference
	response['alias']='treat17'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/treat/treat.djt',response)

def treatabout(request):
	conference = Conference.objects.get(conference_alias='treat17')
	response={}
	response['conference']=conference
	response['alias']='treat17'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/treat/about.djt',response)

def treatlinks(request):
	conference = Conference.objects.get(conference_alias='treat17')
	response={}
	response['conference']=conference
	response['alias']='treat17'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/treat/links.djt',response)

@login_required(login_url='/signin/mmse2018')
def reupload_paper(request,alias):
	conference = Conference.objects.get(conference_alias=alias)
	now = datetime.datetime.now()
	if request.method == 'POST' :
		paper = Conf_Paper.objects.get(paper_id=request.POST['paperid'],uid=request.user)
		paper.paperfile=request.FILES['paper_file']
		if not validateFormat(paper.paperfile) :
				return HttpResponse('Only Pdf format is allowed')
		# paper.submissionDate=now.strftime("%Y-%m-%d")
		paper.submissionDate=now
		paper.status = 0
		paper.revisionNumber += 1
		paper.save()
	url = '/conference/'+conference.conference_alias+"/dashboard/"
	return redirect(url)	

@login_required(login_url='/signin/mmse2018')
def final_paper(request,alias):
	conference = Conference.objects.get(conference_alias=alias)
	now = datetime.datetime.now()
	if request.method == 'POST' :
		papername = request.POST['paper_name']
		paper = Conf_Paper.objects.get(paper_id=request.POST['paper'],uid=request.user)
		copyright_form = request.FILES['copyright_form']
		final_paper = request.FILES['final_paper']
		if not validateFormat(final_paper) :
				return HttpResponse('Only Pdf format is allowed')

		finalpaper = Final_paper()
		finalpaper.papername = papername
		finalpaper.related_paper = paper
		finalpaper.final_file = final_paper
		finalpaper.copyright_form = copyright_form
		finalpaper.save()

	url = '/conference/'+conference.conference_alias+"/dashboard/"
	return redirect(url)


def nhtff(request):
	conference = Conference.objects.get(conference_alias='nhtff2018')
	response = {}
	response['conference']=conference
	response['alias']='nhtff2018'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/nhtff/home.djt',response)

def nhtffabout(request):
	conference = Conference.objects.get(conference_alias='nhtff2018')
	response={}
	response['conference']=conference
	response['alias']='nhtff2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/nhtff/about.djt',response)

def nhtfflinks(request):
	conference = Conference.objects.get(conference_alias='nhtff2018')
	response={}
	response['conference']=conference
	response['alias']='nhtff2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/nhtff/links.djt',response)

def mmse(request):
	conference = Conference.objects.get(conference_alias='mmse2018')
	response = {}
	response['conference']=conference
	response['alias']='mmse2018'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/mmse/home.djt',response)

def mmseabout(request):
	conference = Conference.objects.get(conference_alias='mmse2018')
	response={}
	response['conference']=conference
	response['alias']='mmse2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/mmse/about.djt',response)

def mmselinks(request):
	conference = Conference.objects.get(conference_alias='mmse2018')
	response={}
	response['conference']=conference
	response['alias']='mmse2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/mmse/links.djt',response)

def ctsem(request):
	conference = Conference.objects.get(conference_alias='ctsem2018')
	print conference
	print"hai"
	response = {}
	response['conference']=conference
	response['alias']='ctsem2018'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images
	print images
	print request.user.is_authenticated

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/ctsem/home.djt',response)

def ctsemabout(request):
	conference = Conference.objects.get(conference_alias='ctsem2018')
	response={}
	response['conference']=conference
	response['alias']='ctsem2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/ctsem/about.djt',response)

def ctsemlinks(request):
	conference = Conference.objects.get(conference_alias='ctsem2018')
	response={}
	response['conference']=conference
	response['alias']='ctsem2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/ctsem/links.djt',response)

def rames(request):
	conference = Conference.objects.get(conference_alias='rames2018')
	response = {}
	response['conference']=conference
	response['alias']='rames2018'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/rames/home.djt',response)

def ramesabout(request):
	conference = Conference.objects.get(conference_alias='rames2018')
	response={}
	response['conference']=conference
	response['alias']='rames2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/rames/about.djt',response)

def rameslinks(request):
	conference = Conference.objects.get(conference_alias='rames2018')
	response={}
	response['conference']=conference
	response['alias']='rames2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/rames/links.djt',response)

def fccm(request):
	conference = Conference.objects.get(conference_alias='fccm2018')
	response = {}
	response['conference']=conference
	response['alias']='fccm2018'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/fccm/home.djt',response)

def fccmabout(request):
	conference = Conference.objects.get(conference_alias='fccm2018')
	response={}
	response['conference']=conference
	response['alias']='fccm2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/fccm/about.djt',response)

def fccmlinks(request):
	conference = Conference.objects.get(conference_alias='fccm2018')
	response={}
	response['conference']=conference
	response['alias']='fccm2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/fccm/links.djt',response)

@login_required(login_url='/signin/mmse2018')
def metallography_contest(request):
	conference = Conference.objects.get(conference_alias='fccm2018')
	response = {}
	response['conference']=conference
	response['alias']='fccm2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	
	response['filled'] = 0
	if Contest.objects.filter(contestant=request.user).count()>0 :
		response['filled'] = 1

	return render(request, 'conference/contest.djt',response)

@login_required(login_url='/signin/mmse2018')
def registerForContest(request):
	conference = Conference.objects.get(conference_alias='fccm2018')
	if request.method == 'POST' :
		category = request.POST.get('category','')
		zipfile = request.FILES['zipfile']

		contestObj = Contest()
		contestObj.contestant = request.user
		if category == '1':
			contestObj.category = 'Transmission Electron Microscopy (TEM)'
		elif category == '2':
			contestObj.category = 'Scanning Electron Microscopy (SEM)'
		else :
			contestObj.category = 'Other Micrographs'

		contestObj.zipfile = zipfile

		contestObj.save()

	return redirect('/conference/metallography_contest')


## NHTFF Part
# def sendTrackingMail(paper):
# 	#Mail application ID to applicant
# 	receiver = paper.uid.email
# 	sender = 'nhtff2018@nitw.ac.in'

# 	content = "Tracking id : " + paper.paperRefNum+'\n\n'
# 	content += "Title : "+ paper.papername + '\n\n'
# 	content += "Dear Author\n\n"
# 	content += 'Thank you for submitting your manuscript for consideration for publication / presentation at  "International Conference on Numerical Heat Transfer and Fluid Flow". \n\n'
# 	content += 'Your submission was received in good order.\n\n'
# 	content += 'To track the status of your manuscript, please log into Conference website  at: cms.nitw.ac.in/conference/nhtff2018.\n\n'
# 	content += 'Thank you for submitting your work to the conference.\n\n'
# 	content += 'Kind regards,\n\n'
# 	content += 'Dr. D. Srinivasacharya\n\n'
# 	content += 'Conference Chair, NHTFF-2018" \n\n'

# 	rlist = []
# 	rlist.append(receiver)
# 	try:
# 		send_mail('Tracking ID for uploaded paper',content,sender,rlist,fail_silently=False,)
# 	except BadHeaderError:
# 		return HttpResponse('Invalid header found.')

# 	return

def sendTrackingMail(paper,alias):
	#Mail application ID to applicant
	if alias == 'mmse2018' :
		receiver = paper.uid.email
		sender = 'mmse2018.nitw@gmail.com'

		content = "Tracking id : " + paper.paperRefNum+'\n\n'
		content += "Title : "+ paper.papername + '\n\n'
		content += "Dear Author\n\n"
		content += 'Thank you for submitting your manuscript for consideration for publication / presentation at  "National Conference on MATHEMATICAL MODELING IN SCIENCE AND ENGINEERING". \n\n'
		content += 'Your submission was received in good order.\n\n'
		content += 'To track the status of your manuscript, please log into Conference website  at: cms.nitw.ac.in/mmse.\n\n'
		content += 'Thank you for submitting your work to the conference.\n\n'
		content += '\n\n For any queries mail to mmse2018.nitw@gmail.com .\n\n'
		content += 'Kind regards,\n\n'
		content += 'Dr. D. Srinivasacharya\n\n'
		content += 'Conference Chair, MMSE-2018" \n\n'

		rlist = []
		rlist.append(receiver)
		try:
			send_mail('Tracking ID for uploaded paper for conference MMSE-2018',content,sender,rlist,fail_silently=False,)
		except BadHeaderError:
			return HttpResponse('Invalid header found.')

	if alias == 'ctsem2018' :
		receiver = paper.uid.email
		sender = 'ctsem2018@gmail.com'

		content = "Tracking id : " + paper.paperRefNum+'\n\n'
		content += "Title : "+ paper.papername + '\n\n'
		content += "Dear Author\n\n"
		content += 'Thank you for submitting your manuscript for consideration for publication / presentation at  "5th Colloquium on Transportation Systems Engineering and Management". \n\n'
		content += 'Your submission was received in good order.\n\n'
		content += 'To track the status of your manuscript, please log into Conference website  at: cms.nitw.ac.in/ctsem.\n\n'
		content += 'Thank you for submitting your work to the conference.\n\n'
		content += '\n\n For any queries mail to ctsem2018@gmail.com .\n\n'
		content += 'Kind regards,\n\n'
		content += 'Prof. C.S.R.K. Prasad\n\n'
		content += 'Colloquium Chair, CTSEM-2018" \n\n'

		rlist = []
		rlist.append(receiver)
		try:
			send_mail('Tracking ID for uploaded paper for conference CTSEM-2018',content,sender,rlist,fail_silently=False,)
		except BadHeaderError:
			return HttpResponse('Invalid header found.')

	if alias == 'fccm2018' :
		receiver = paper.uid.email
		sender = 'fccm2018nitw@gmail.com'

		content = "Tracking id : " + paper.paperRefNum+'\n\n'
		content += "Title : "+ paper.papername + '\n\n'
		content += "Dear Author\n\n"
		content += 'Thank you for submitting your manuscript for consideration for publication / presentation at  "National Conference on Frontiers in Corrosion Control of Materials". \n\n'
		content += 'Your submission was received in good order.\n\n'
		content += 'To track the status of your manuscript, please log into Conference website  at: cms.nitw.ac.in/fccm.\n\n'
		content += 'Thank you for submitting your work to the conference.\n\n'
		content += '\n\n For any queries mail to fccm2018nitw@gmail.com .\n\n'
		content += 'Kind regards,\n\n'
		content += 'Prof. G. V. S. Nageswara Rao\n\n'
		content += 'Conference Convener, FCCM-2018" \n\n'

		rlist = []
		rlist.append(receiver)
		try:
			send_mail('Tracking ID for uploaded paper for conference FCCM-2018',content,sender,rlist,fail_silently=False,)
		except BadHeaderError:
			return HttpResponse('Invalid header found.')

	if alias == 'inceee2019' :
		receiver = paper.uid.email
		sender = 'inceee2019@gmail.com'

		content = "Paper ID : " + paper.paperRefNum+'\n\n'
		content += "Title : "+ paper.papername + '\n\n'
		content += "Dear Author\n\n"
		content += 'Thank you for submitting your abstract for INCEEE2019. \n\n'
		content += 'Your submission was received in good order.\n\n'
		content += 'To track the status of your submission, please login into Conference website  at: cms.nitw.ac.in/inceee2019 and go to uploadPaper tab. \n\n'
		content += 'In any future correspondence please mention your Paper ID.\n\n'
		content += 'The acceptance of your submission will be notified by email.\n\n'
		content += '\nFor any queries mail to inceee2019@gmail.com .\n\n'
		content += 'Kind regards,\n\n'
		content += 'Department of Chemical Engineering,\n'
		content += 'National Institute of Technology,\nWarangal - 506 004, Telangana State, India. \n'
		content += 'Mobile: +91-8332969396, 402, 403'
		rlist = []
		rlist.append(receiver)
		try:
			send_mail('Paper ID for uploaded paper for conference INCEEE-2019',content,sender,rlist,fail_silently=False,)
		except BadHeaderError:
			return HttpResponse('Invalid header found.')

	return


# CMFDP
def cmfdp(request):
	conference = Conference.objects.get(conference_alias='cmfdp2019')
	print conference
	print"hai"
	response = {}
	response['conference']=conference
	response['alias']='cmfdp2019'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images
	print images
	print request.user.is_authenticated

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		print payment
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/cmfdp/home.djt',response)

def cmfdpabout(request):
	conference = Conference.objects.get(conference_alias='cmfdp2019')
	response={}
	response['conference']=conference
	response['alias']='cmfdp2019'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/cmfdp/about.djt',response)

def cmfdplinks(request):
	conference = Conference.objects.get(conference_alias='cmfdp2019')
	response={}
	response['conference']=conference
	response['alias']='cmfdp2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/cmfdp/links.djt',response)

#ewcti
def ewcti(request):
	conference = Conference.objects.get(conference_alias='ewcti2018')
	print conference
	response = {}
	response['conference']=conference
	response['alias']='ewcti2018'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images
	print images
	print request.user.is_authenticated

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		print payment
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/ewcti/home.djt',response)

def ewctiabout(request):
	conference = Conference.objects.get(conference_alias='ewcti2018')
	response={}
	response['conference']=conference
	response['alias']='ewcti2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/ewcti/about.djt',response)

def ewctilinks(request):
	conference = Conference.objects.get(conference_alias='ewcti2018')
	response={}
	response['conference']=conference
	response['alias']='ewcti2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/ewcti/links.djt',response)

def ewctihotels(request):
	conference = Conference.objects.get(conference_alias='ewcti2018')
	response={}
	response['conference']=conference
	response['alias']='ewcti2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/ewcti/hotels.djt',response)

@login_required(login_url='/signin/ewcti2019')
def ewctiapply(request):
	conference = Conference.objects.get(conference_alias='ewcti2018')
	response={}
	response['conference']=conference
	response['alias']='ewcti2018'
	payment = Payment.objects.filter(user=request.user, conf_id=conference)
	# print payment.is_aprooved
	if len(payment)==1 :
		response['payment'] = payment.first()

	if request.method == 'POST' :
		now = datetime.datetime.now()
		applyConf = request.POST.get('applyConf','off')
		print applyConf
		if applyConf == 'on':
			# apply only if no request is present.
			if  Conf_Paper.objects.filter(uid=request.user, conf_id=conference).count() == 0:
				regconf = Registered_Conference()
				regconf.conf_id = conference
				regconf.user = request.user
				regconf.save()
				paper = Conf_Paper()
				paper.conf_id=conference
				paper.uid=request.user
				paper.papername="Applying for conference"
				paper.submissionDate = now
				paper.status = 0
				conference.paperCount += 1
				conference.save()

				count = 30
				tempRefnum = '18'+str(randint(1000, 9999))
				if Conf_Paper.objects.filter(paperRefNum=tempRefnum).count() > 0 :
					print "existing refnum"
					while count > 0:
						tempRefnum = '18'+str(randint(1000, 9999))
						if Conf_Paper.objects.filter(paperRefNum=tempRefnum).count() > 0 :
							count -= 1
							continue
						else:
							break
				if count==0:
					count = 1
					tempRefnum = '18' + str(count).zfill(4)
					while Conf_Paper.objects.filter(paperRefNum=temprefnum).count() > 0 :
						count += 1
						tempRefnum = '18' + str(count).zfill(4)
				
				paper.paperRefNum = tempRefnum
				paper.save()
				regconf.papers.add(paper)
				regconf.save()
	try:
		paper = Conf_Paper.objects.get(uid=request.user, conf_id=conference)
		response['paper'] = paper
	except:
		response['nopaper'] = True

	return render(request, 'conference/ewcti/apply.djt',response)

def ewctiprofiles(request):
	conference = Conference.objects.get(conference_alias='ewcti2018')
	response={}
	response['conference']=conference
	response['alias']='ewcti2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/ewcti/profiles.djt',response)


#tssc2018
def tssc(request):
	conference = Conference.objects.get(conference_alias='tssc2018')
	print conference
	print"hai"
	response = {}
	response['conference']=conference
	response['alias']='tssc2018'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images
	print images
	print request.user.is_authenticated

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		print payment
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/tssc/home.djt',response)

def tsscabout(request):
	conference = Conference.objects.get(conference_alias='tssc2018')
	response={}
	response['conference']=conference
	response['alias']='tssc2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/tssc/about.djt',response)

def tssclinks(request):
	conference = Conference.objects.get(conference_alias='tssc2018')
	response={}
	response['conference']=conference
	response['alias']='tssc2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/tssc/links.djt',response)

def tsschotels(request):
	conference = Conference.objects.get(conference_alias='tssc2018')
	response={}
	response['conference']=conference
	response['alias']='tssc2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/tssc/hotels.djt',response)
	return render(request, 'conference/ewcti/profiles.djt',response)

def get_temp_ref_num():
	count = 30
	tempRefnum = '18'+str(randint(1000, 9999))
	if Conf_Paper.objects.filter(paperRefNum=tempRefnum).count() > 0 :
		print "existing refnum"
		while count > 0:
			tempRefnum = '18'+str(randint(1000, 9999))
			if Conf_Paper.objects.filter(paperRefNum=tempRefnum).count() > 0 :
				count -= 1
				continue
			else:
				break
	if count==0:
		count = 1
		tempRefnum = '18' + str(count).zfill(4)
		while Conf_Paper.objects.filter(paperRefNum=temprefnum).count() > 0 :
			count += 1
			tempRefnum = '18' + str(count).zfill(4)
	return tempRefnum

@login_required(login_url='/signin/tssc2018')
def tsscapply(request):
	conference = Conference.objects.get(conference_alias='tssc2018')
	
	response={}
	response['conference'] = conference
	response['alias'] = 'tssc2018'
	name = request.user.first_name + " " + request.user.last_name
	response['name'] = name
	response['email'] = request.user.email
	response['mobile'] = request.user.profile.contact
	response['designation'] = request.user.profile.designation

	payment = Payment.objects.filter(user=request.user, conf_id=conference)
	# print payment.is_aprooved
	if len(payment)==1 :
		response['payment'] = payment.first()

	if request.method == 'POST' :
		now = datetime.datetime.now()
		applyConf = request.POST.get('applyConf','off')
		print applyConf
		if applyConf == 'on':
			# apply only if no request is present.
			if  Conf_Paper.objects.filter(uid=request.user, conf_id=conference).count() == 0:
				regconf = Registered_Conference()
				regconf.conf_id = conference
				regconf.user = request.user
				paper = Conf_Paper()
				paper.conf_id=conference
				paper.uid=request.user
				paper.papername=request.POST.get('papername', 'Applying for conference')
				paper.submissionDate = now
				paper.themes = ','.join(str(e) for e in request.POST.getlist('themes', []))
				paper.status = 0
				if request.FILES.get('file', None) is None:
						return HttpResponse('Please upload abstract document. Press back button to try again.')
				paper.paperfile=request.FILES.get('file', None)
				if not validateFormat(paper.paperfile) :
						return HttpResponse('Only PDF format is allowed for abstract submission. Press back button to try again.')
				regconf.save()
				conference.paperCount += 1
				conference.save()

				tempRefnum = get_temp_ref_num()
				paper.paperRefNum = tempRefnum

				profile = request.user.profile
				profile.affiliation = request.POST.get('affiliation', '')
				profile.address = request.POST.get('address', '')
				profile.save()

				paper.save()
				regconf.papers.add(paper)
				regconf.save()
	try:
		paper = Conf_Paper.objects.get(uid=request.user, conf_id=conference)
		response['paper'] = paper
	except:
		response['nopaper'] = True
	return render(request, 'conference/tssc/apply.djt',response)

#noieas
def noieas(request):
	conference = Conference.objects.get(conference_alias='NOIEAS-2019')
	print conference
	response = {}
	response['conference']=conference
	response['alias']='NOIEAS-2019'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images
	print images
	print request.user.is_authenticated

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		print payment
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/noieas/home.djt',response)

def noieasabout(request):
	conference = Conference.objects.get(conference_alias='NOIEAS-2019')
	response={}
	response['conference']=conference
	response['alias']='NOIEAS-2019'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/noieas/about.djt',response)

def noieaslinks(request):
	conference = Conference.objects.get(conference_alias='NOIEAS-2019')
	response={}
	response['conference']=conference
	response['alias']='NOIEAS-2019'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/noieas/links.djt',response)

def noieashotels(request):
	conference = Conference.objects.get(conference_alias='NOIEAS-2019')
	response={}
	response['conference']=conference
	response['alias']='NOIEAS-2019'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/noieas/hotels.djt',response)

@login_required(login_url='/signin/NOIEAS-2019')
def noieasapply(request):
	conference = Conference.objects.get(conference_alias='NOIEAS-2019')
	response={}
	response['conference']=conference
	response['alias']='NOIEAS-2019'
	payment = Payment.objects.filter(user=request.user, conf_id=conference)
	# print payment.is_aprooved
	if len(payment)==1 :
		response['payment'] = payment.first()
	if  Registered_Conference.objects.filter(user=request.user, conf_id=conference).count() > 0:
			response['paper'] = True
	if request.method == 'POST' :
		now = datetime.datetime.now()
		applyConf = request.POST.get('applyConf','off')
		print applyConf
		if applyConf == 'on':
			# apply only if no request is present.
			if  Registered_Conference.objects.filter(user=request.user, conf_id=conference).count() == 0:
				regconf = Registered_Conference()
				regconf.conf_id = conference
				regconf.user = request.user
				regconf.save()
				# paper = Conf_Paper()
				# paper.conf_id=conference
				# paper.uid=request.user
				# paper.papername="Applying for conference"
				# paper.submissionDate = now
				# paper.status = 0
				# conference.paperCount += 1
				conference.save()

				# count = 30
				# tempRefnum = '18'+str(randint(1000, 9999))
				# if Conf_Paper.objects.filter(paperRefNum=tempRefnum).count() > 0 :
				# 	print "existing refnum"
				# 	while count > 0:
				# 		tempRefnum = '18'+str(randint(1000, 9999))
				# 		if Conf_Paper.objects.filter(paperRefNum=tempRefnum).count() > 0 :
				# 			count -= 1
				# 			continue
				# 		else:
				# 			break
				# if count==0:
				# 	count = 1
				# 	tempRefnum = '18' + str(count).zfill(4)
				# 	while Conf_Paper.objects.filter(paperRefNum=temprefnum).count() > 0 :
				# 		count += 1
				# 		tempRefnum = '18' + str(count).zfill(4)
				
				# paper.paperRefNum = tempRefnum
				# paper.save()
				# regconf.papers.add(paper)
				# regconf.save()
				response['paper'] = True
			else:
				# try:
					# paper = Conf_Paper.objects.get(uid=request.user, conf_id=conference)
				response['paper'] = True
				# except:
				# 	response['nopaper'] = True
		# else:
		# 	if  Registered_Conference.objects.filter(user=request.user, conf_id=conference).count() != 0:
		# 		response['paper'] = True
		# 	else:
		# 		response['paper'] = False
	return render(request, 'conference/noieas/apply.djt',response)


#####################icee2019 starting page###########################################################################
def inceee(request):
	print "INCEEE-2019"
	conference = Conference.objects.get(conference_alias='inceee2019')
	print conference
	print"hai"
	response = {}
	response['conference']=conference
	response['alias']='inceee2019'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images
	print images
	print request.user.is_authenticated

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		print payment
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/inceee/home.djt',response)

def inceeeabout(request):
	conference = Conference.objects.get(conference_alias='inceee2019')
	response={}
	response['conference']=conference
	response['alias']='inceee2019'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/inceee/about.djt',response)

def inceeelinks(request):
	conference = Conference.objects.get(conference_alias='inceee2019')
	response={}
	response['conference']=conference
	response['alias']='tssc2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/inceee/links.djt',response)

def inceeehotels(request):
	conference = Conference.objects.get(conference_alias='inceee2019')
	response={}
	response['conference']=conference
	response['alias']='inceee2019'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/inceee/hotels.djt',response)

@login_required(login_url='/signin/inceee2019')
def inceeeapply(request):
	conference = Conference.objects.get(conference_alias='inceee2019')
	print conference.alias
	response={}
	response['conference'] = conference
	response['alias'] = 'inceee2019'
	name = request.user.first_name + " " + request.user.last_name
	response['name'] = name
	response['email'] = request.user.email
	response['mobile'] = request.user.profile.contact
	response['designation'] = request.user.profile.designation

	payment = Payment.objects.filter(user=request.user, conf_id=conference)
	# print payment.is_aprooved
	if len(payment)==1 :
		response['payment'] = payment.first()

	if request.method == 'POST' :
		now = datetime.datetime.now()
		applyConf = request.POST.get('applyConf','off')
		print applyConf
		if applyConf == 'on':
			# apply only if no request is present.
			if  Conf_Paper.objects.filter(uid=request.user, conf_id=conference).count() == 0:
				regconf = Registered_Conference()
				regconf.conf_id = conference
				regconf.user = request.user
				paper = Conf_Paper()
				paper.conf_id=conference
				paper.uid=request.user
				paper.papername=request.POST.get('papername', 'Applying for conference')
				paper.submissionDate = now
				paper.themes = ','.join(str(e) for e in request.POST.getlist('themes', []))
				paper.status = 0
				if request.FILES.get('file', None) is None:
						return HttpResponse('Please upload abstract document. Press back button to try again.')
				paper.paperfile=request.FILES.get('file', None)
				if not validateFormat(paper.paperfile) :
						return HttpResponse('Only PDF format is allowed for abstract submission. Press back button to try again.')
				regconf.save()
				conference.paperCount += 1
				conference.save()

				tempRefnum = get_temp_ref_num()
				paper.paperRefNum = tempRefnum

				profile = request.user.profile
				profile.affiliation = request.POST.get('affiliation', '')
				profile.address = request.POST.get('address', '')
				profile.save()

				paper.save()
				regconf.papers.add(paper)
				regconf.save()
	try:
		paper = Conf_Paper.objects.get(uid=request.user, conf_id=conference)
		response['paper'] = paper
	except:
		response['nopaper'] = True
	return render(request, 'conference/inceee/apply.djt',response)

def inceeeaccomodation(request):
	response = {}
	houses = Accomodation.objects.all()
	conference = Conference.objects.get(conference_alias='inceee2019')
	response["conference"] = conference
	response["houses"] = houses
	if request.method == "POST":
		house = request.POST["house"]
		Name = request.POST["Name"]
		email = request.POST["email"]
		paper_id = request.POST["paper_id"]
		house = Accomodation.objects.get(houseName=house)
		slip = request.FILES.get("pay_receipt","")
		startDate = request.POST["startDate"]
		endDate = request.POST["endDate"]
		payment = AccomodationPayment()
		payment.Name = Name
		payment.paper_id = paper_id
		payment.reference_number = request.POST["refno"]
		conf = Conference.objects.get(conference_alias='inceee2019')
		payment.conf_id = conf
		payment.payment_receipt = slip
		payment.house_choice = house
		payment.start_date = startDate
		payment.end_date = endDate
		payment.email = email
		payment.save()
		print type(house)
	return render(request,'conference/inceee/accomodation.djt', response)



########################################################### SEP - 2019 ###############################################################


def sep(request):
	conference = Conference.objects.get(conference_alias='sep2019')
	print conference
	print"hai"
	response = {}
	response['conference']=conference
	response['alias']='sep2019'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images
	print images
	print request.user.is_authenticated

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		print payment
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/sep/home.djt',response)
# def sep(request):
# 	print "INCEEE-2019"
# 	conference = Conference.objects.get(conference_alias='sep2019')
# 	print conference
# 	print"hai"
# 	response = {}
# 	response['conference']=conference
# 	response['alias']='sep2019'


def sepabout(request):
	conference = Conference.objects.get(conference_alias='sep2019')
	response={}
	response['conference']=conference
	response['alias']='sep2019'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/sep/about.djt',response)

def seplinks(request):
	conference = Conference.objects.get(conference_alias='sep2019')
	response={}
	response['conference']=conference
	response['alias']='tssc2018'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/sep/links.djt',response)

def sephotels(request):
	conference = Conference.objects.get(conference_alias='sep2019')
	response={}
	response['conference']=conference
	response['alias']='sep2019'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/sep/hotels.djt',response)

@login_required(login_url='/signin/sep2019')
def sepapply(request):
	conference = Conference.objects.get(conference_alias='sep2019')
	response={}
	response['conference']=conference
	response['alias']='sep2019'
	payment = Payment.objects.filter(user=request.user, conf_id=conference)
	# print payment.is_aprooved
	if len(payment)==1 :
		response['payment'] = payment.first()

	if request.method == 'POST' :
		now = datetime.datetime.now()
		applyConf = request.POST.get('applyConf','off')
		print applyConf
		if applyConf == 'on':
			# apply only if no request is present.
			if  Registered_Conference.objects.filter(user=request.user, conf_id=conference).count() == 0:
				regconf = Registered_Conference()
				regconf.conf_id = conference
				regconf.user = request.user
				regconf.save()
				conference.save()
				response['paper'] = True
		else:
				response['paper'] = False
	return render(request, 'conference/sep/apply.djt',response)


########################################################### ICAMER - 2019 ###############################################################

def icamer(request):
	print "ICAMER-2019"
	alias = 'icamer2019'
	conference = Conference.objects.get(conference_alias=alias)
	print conference
	response = {}
	response['conference']=conference
	response['alias']=alias
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images
	print images
	print request.user.is_authenticated

	if request.user.is_authenticated :
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		print payment
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/icamer/home.djt',response)


def icamerabout(request):
	alias = 'icamer2019'
	conference = Conference.objects.get(conference_alias=alias)
	response={}
	response['conference']=conference
	response['alias']=alias
	if request.user.is_authenticated :
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/icamer/about.djt',response)

def icamerlinks(request):
	alias = 'icamer2019'
	conference = Conference.objects.get(conference_alias=alias)
	response={}
	response['conference']=conference
	response['alias']=alias
	if request.user.is_authenticated :
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/icamer/links.djt',response)

def icamerhotels(request):
	alias = 'icamer2019'
	conference = Conference.objects.get(conference_alias=alias)
	response= {'conference': conference, 'alias': alias}
	if request.user.is_authenticated :
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/icamer/hotels.djt',response)

def icamerdates(request):
	alias = 'icamer2019'
	conference = Conference.objects.get(conference_alias=alias)
	response = {'conference': conference, 'alias': alias}
	if request.user.is_authenticated:
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment) == 1:
			response['payment'] = payment
	return render(request, 'conference/icamer/dates.djt', response)

def icamerfees(request):
	alias = 'icamer2019'
	conference = Conference.objects.get(conference_alias=alias)
	response = {'conference': conference, 'alias': alias}
	if request.user.is_authenticated:
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment) == 1:
			response['payment'] = payment
	return render(request, 'conference/icamer/fee_details.djt', response)


@login_required(login_url='/signin/icamer2019')
def icamerapply(request):
	alias='icamer2019'
	conference = Conference.objects.get(conference_alias=alias)
	print conference.alias
	response={}
	response['conference'] = conference
	response['alias'] = alias
	name = request.user.first_name + " " + request.user.last_name
	response['name'] = name
	response['email'] = request.user.email
	response['mobile'] = request.user.profile.contact
	response['designation'] = request.user.profile.designation

	payment = Payment.objects.filter(user=request.user, conf_id=conference)
	# print payment.is_aprooved
	if len(payment)==1 :
		response['payment'] = payment.first()

	if request.method == 'POST' :
		now = datetime.datetime.now()
		applyConf = request.POST.get('applyConf','off')
		print applyConf
		if applyConf == 'on':
			# apply only if no request is present.
			if  Conf_Paper.objects.filter(uid=request.user, conf_id=conference).count() == 0:
				regconf = Registered_Conference()
				regconf.conf_id = conference
				regconf.user = request.user
				paper = Conf_Paper()
				paper.conf_id=conference
				paper.uid=request.user
				paper.papername=request.POST.get('papername', 'Applying for conference')
				paper.submissionDate = now
				paper.themes = ','.join(str(e) for e in request.POST.getlist('themes', []))
				paper.status = 0
				if request.FILES.get('file', None) is None:
						return HttpResponse('Please upload abstract document. Press back button to try again.')
				paper.paperfile=request.FILES.get('file', None)
				if not validateFormat(paper.paperfile) :
						return HttpResponse('Only PDF format is allowed for abstract submission. Press back button to try again.')
				regconf.save()
				conference.paperCount += 1
				conference.save()

				tempRefnum = get_temp_ref_num()
				paper.paperRefNum = tempRefnum

				profile = request.user.profile
				profile.affiliation = request.POST.get('affiliation', '')
				profile.address = request.POST.get('address', '')
				profile.save()

				paper.save()
				regconf.papers.add(paper)
				regconf.save()
	try:
		paper = Conf_Paper.objects.get(uid=request.user, conf_id=conference)
		response['paper'] = paper
	except:
		response['nopaper'] = True
	return render(request, 'conference/icamer/apply.djt',response)


# ITCSD
def itcsd(request):
	conference = Conference.objects.get(conference_alias='itcsd2019')
	print conference
	print"hai"
	response = {}
	response['conference']=conference
	response['alias']='itcsd2019'
	images = Conf_Image.objects.filter(conf_id=conference)
	response['images']=images
	print images
	print request.user.is_authenticated

	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		print payment
		if len(payment)==1 :
			response['payment'] = payment[0]

	return render(request, 'conference/itcsd/home.djt',response)

def itcsdabout(request):
	conference = Conference.objects.get(conference_alias='itcsd2019')
	response={}
	response['conference']=conference
	response['alias']='itcsd2019'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/itcsd/about.djt',response)

def itcsdlinks(request):
	conference = Conference.objects.get(conference_alias='itcsd2019')
	response={}
	response['conference']=conference
	response['alias']='itcsd2019'
	if request.user.is_authenticated : 
		payment = Payment.objects.filter(user=request.user, conf_id=conference)
		if len(payment)==1 :
			response['payment'] = payment
	return render(request, 'conference/itcsd/links.djt',response)

#NITW GIAN SITE SINGLE PAGE RENDERING 
def gian(request):
	return render(request, 'conference/gian/home.djt')

