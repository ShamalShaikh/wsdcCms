from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from conference.models import *
from django.core.files.storage import FileSystemStorage
from django.conf import settings

sendfile_storage = FileSystemStorage(location=settings.SENDFILE_ROOT)

def get_user_profile_picture_path(instance,filename):
    return 'userprofile/{0}'.format(filename)

def get_dd_path(instance,filename):
	return 'payments/{0}/{1}'.format("".join(instance.conf_id.conference_name.split()),filename)

def get_adv_path(instance,filename):
	return 'spons/{0}/{1}'.format("".join(instance.conf.conference_name.split()),filename)

def validate(value):
	    import os
	    ext = os.path.splitext(value.name)[1]
	    valid_extentions = ['.pdf']
	    if not ext in valid_extentions:
	        raise ValidationError(u'File type is not supported')

class Payment(models.Model):
	payment_choice = (
		('net','Net Banking'),
		('dd','Through DD'),
	)
	user = models.ForeignKey(User)
	conf_id = models.ForeignKey(Conference)
	amount = models.IntegerField(default=0)
	payment_mode = models.CharField(max_length=20,choices=payment_choice)
	pic_of_dd = models.ImageField(upload_to=get_dd_path,null=True,blank=True,storage=sendfile_storage)
	pic_of_id = models.ImageField(upload_to=get_dd_path,null=True,blank=True,storage=sendfile_storage)
	is_aprooved = models.BooleanField(default=False)
	is_rejected = models.BooleanField(default=False)
	remarks = models.CharField(max_length=50,null=True,blank=True)
	date = models.DateField(null=True)

	def __unicode__(self):
		return (self.user.username+" for "+self.conf_id.conference_name)


class Registered_Conference(models.Model):
	conf_id = models.ForeignKey(Conference)
	papers = models.ManyToManyField(Conf_Paper,blank=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return (self.user.username+" --> "+self.conf_id.conference_name)

class Alumani(models.Model):
	degree = models.CharField(max_length=255, blank=True)
	year = models.CharField(max_length=255, blank=True)
	branch = models.CharField(max_length=255, blank=True)

	def __unicode__(self):
		return self.year + "_" + self.branch

class UserProfile(models.Model):
	user = models.OneToOneField(User,related_name='profile')
	contact = models.CharField(max_length=20,null=True)
	institute = models.CharField(max_length=255,null=True)
	profilepic = models.ImageField(upload_to=get_user_profile_picture_path ,null=True, blank=True)
	gender = models.CharField(max_length=10,null=True)
	regConferences = models.ManyToManyField(Registered_Conference,blank=True)
	department = models.CharField(max_length=255,null=True,blank=True)
	designation = models.CharField(max_length=255, blank=True)
	qualification = models.CharField(max_length=255, blank=True)
	alumani = models.ForeignKey(Alumani, null = True)


	def __unicode__(self):
		return self.user.username

class SponsorProfile(models.Model):
	user = models.OneToOneField(User,related_name='sponsProfile')
	conf = models.ForeignKey(Conference, null = True)
	orgName = models.CharField(max_length=255,null=False)
	orgType = models.CharField(max_length=255,null=True)
	md_cco = models.CharField(max_length=255,null=False)
	address1 = models.CharField(max_length=255,null=False)
	address2 = models.CharField(max_length=255,null=True)
	contact = models.CharField(max_length=20,null=False)
	category = models.CharField(max_length=255,null=False)
	advertisement = models.FileField(upload_to=get_adv_path, validators=[validate], null=True, blank=True)

	def __unicode__(self):
		return self.orgName

class Delegates(models.Model):
	sponsor = models.ForeignKey(SponsorProfile)
	name = models.CharField(max_length=255,null=False)
	delegate = models.CharField(max_length=255,null=False)
	contact = models.CharField(max_length=15,null=False)
	email = models.CharField(max_length=63,null=False)

	def __unicode__(self):
		return self.name

class Rejected_payment(models.Model):
	conf_id = models.ForeignKey(Conference)
	user = models.ForeignKey(User)
	pic_of_dd = models.ImageField(upload_to=get_dd_path,null=True,blank=True,storage=sendfile_storage)
	date = models.DateField()
	remarks = models.CharField(max_length=50,null=True,blank=True)

	def __unicode__(self):
		return (self.user.username+" for "+self.conf_id.conference_name+" - "+self.date.strftime("%Y-%m-%d"))
