from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from login_auth.models import *
from manager.models import Manager
from django.core.files.storage import FileSystemStorage
from django.conf import settings

sendfile_storage = FileSystemStorage(location=settings.SENDFILE_ROOT)

# Create your models here.
def get_conf_image_path(instance,filename):
    return 'conference_images/{0}/{1}'.format("".join(instance.conf_id.conference_name.split()),filename)

def get_conf_paper_path(instance,filename):
	return 'conference_papers/{0}/{1}'.format("".join(instance.conf_id.conference_name.split()),filename)

def get_final_paper_path(instance,filename):
	return 'conference_papers/final_papers/{0}/{1}'.format("".join(instance.related_paper.conf_id.conference_name.split()),filename)

def get_remark_file_path(instance,filename):
	return 'conference_papers/remarks/{0}/{1}'.format("".join(instance.conf_paper.conf_id.conference_name.split()),filename)

def get_zip_file_path(instance,filename):
	return 'conference_zips/{0}/{1}'.format("".join(instance.contestant.username.split()),filename)

def validate(value):
	    import os
	    ext = os.path.splitext(value.name)[1]
	    valid_extentions = ['.pdf']
	    if not ext in valid_extentions:
	        raise ValidationError(u'File type is not supported')

class Branch(models.Model):
	branch_name = models.CharField(max_length=200)
	branch_alias = models.CharField(max_length=10)
	def __unicode__(self):
		return self.branch_name

class Conference(models.Model):
	conference_id = models.AutoField(primary_key = True)
	conference_name = models.CharField(max_length = 100)
	conference_alias = models.CharField(max_length = 50,null=True,blank=True)
	startDate = models.DateField()
	endDate = models.DateField()
	is_published = models.BooleanField(default = False)
	description = models.CharField(max_length = 200)
	alias = models.CharField(max_length = 10)
	manager = models.ForeignKey(Manager)
	fee = models.IntegerField(default=0)
	max_papers = models.IntegerField(default=1)
	branch = models.ForeignKey(Branch,null=True,blank=True)
	paperCount = models.IntegerField(default=0)
	def __str__(self):
		return str(self.conference_name)

class Conf_Image(models.Model):
	imgfile = models.ImageField(upload_to=get_conf_image_path ,null=True, blank=True)
	imgname = models.CharField(max_length=20)
	conf_id = models.ForeignKey(Conference, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.imgname+" "+self.conf_id.conference_name)


class Conf_Paper(models.Model):
	paper_id = models.AutoField(primary_key = True)
	paperRefNum = models.CharField(max_length=15,blank=True)
	papername = models.CharField(max_length=250)
	conf_id = models.ForeignKey(Conference, on_delete = models.CASCADE)
	uid = models.ForeignKey(User,on_delete = models.CASCADE, related_name='paper')
	description = models.CharField(max_length = 100)
	themes = models.CharField(max_length=1000, blank=True)
	submissionDate = models.DateTimeField()
	is_approved = models.BooleanField(default=False)
	is_rejected = models.BooleanField(default=False)
	under_review = models.BooleanField(default=False)
	status = models.IntegerField(default=0)
	# 0 - under_review, 1 - revision, 2-approved_for_presentation, 3 - approved for publication
	# 4 - rejected
	revisionNumber = models.IntegerField(default=1)
	paperfile = models.FileField(upload_to=get_conf_paper_path, validators=[validate], null=True, blank=True,storage=sendfile_storage)

	def __str__(self):
	    return str(self.uid)

class Final_paper(models.Model):
	papername = models.CharField(max_length=50)
	related_paper = models.OneToOneField(Conf_Paper, on_delete = models.CASCADE)
	copyright_form = models.FileField(upload_to=get_final_paper_path, validators=[validate], null=True, blank=True,storage=sendfile_storage)
	final_file = models.FileField(upload_to=get_final_paper_path, validators=[validate], null=True, blank=True,storage=sendfile_storage)

	def __str__(self):
	    return str(self.papername)

class Paper_Remark(models.Model):
	manager = models.ForeignKey(Manager)
	content = models.TextField()
	remarkFile = models.FileField(upload_to=get_remark_file_path, validators=[validate], null=True, blank=True,storage=sendfile_storage)
	conf_paper = models.ForeignKey(Conf_Paper, related_name='remark')
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return str(str(self.manager) + " " + self.content[:20] + "....")

class Contest(models.Model):
	contestant = models.ForeignKey(User,on_delete = models.CASCADE)
	category = models.CharField(max_length=255)
	zipfile = models.FileField(upload_to=get_zip_file_path, null=True, blank=True)

	def __str__(self):
		return str(self.contestant.username)
