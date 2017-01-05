from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from login_auth.models import *
from manager.models import Manager

# Create your models here.
def get_conf_image_path(instance,filename):
    return 'conference_images/{0}/{1}'.format(instance.conf_id.conference_name,filename)

def get_conf_paper_path(instance,filename):
	return 'conference_papers/{0}/{1}'.format(instance.conf_id.conference_name,filename)

def validate(value):
	    import os
	    ext = os.path.splitext(value.name)[1]
	    valid_extentions = ['.pdf','.doc','.docx']
	    if not ext in valid_extentions:
	        raise ValidationError(u'File type is not supported')

class Branch(models.Model):
	branch_name = models.CharField(max_length=200)
	branch_alias = models.CharField(max_length=10)
	def __unicode__(self):
		return self.branch_name

class Conference(models.Model):
	conference_id = models.AutoField(primary_key = True)
	conference_name = models.CharField(max_length = 50)
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
	papername = models.CharField(max_length=20)
	conf_id = models.ForeignKey(Conference, on_delete = models.CASCADE)
	uid = models.ForeignKey(User,on_delete = models.CASCADE)
	description = models.CharField(max_length = 100)
	submissionDate = models.DateField()
	is_approved = models.BooleanField(default=False)
	is_rejected = models.BooleanField(default=False)
	under_review = models.BooleanField(default=False)
	paperfile = models.FileField(upload_to=get_conf_paper_path, validators=[validate], null=True, blank=True)

	def __str__(self):
	    return str(self.papername)


class Paper_Remark(models.Model):
	manager = models.ForeignKey(Manager)
	content = models.TextField()
	conf_paper = models.ForeignKey(Conf_Paper)
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return str(str(self.manager) + " " + self.content[:20] + "....")