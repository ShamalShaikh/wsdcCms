from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from conference.models import *


def get_user_profile_picture_path(instance,filename):
    return 'userprofile/{0}'.format(filename)

def get_dd_path(instance,filename):
	return 'payments/{0}/{1}'.format(instance.conf_id.conference_name,filename)

class Payment(models.Model):
	payment_choice = (
		('net','Net Banking'),
		('dd','Through DD'),
	)
	user = models.ForeignKey(User)
	conf_id = models.ForeignKey(Conference)
	amount = models.IntegerField(default=0)
	payment_mode = models.CharField(max_length=20,choices=payment_choice)
	pic_of_dd = models.ImageField(upload_to=get_dd_path,null=True,blank=True)
	is_aprooved = models.BooleanField(default=False)
	is_rejected = models.BooleanField(default=False)
	remarks = models.CharField(max_length=50,null=True,blank=True)

	def __unicode__(self):
		return (self.user.username+" for "+self.conf_id.conference_name)


class Registered_Conference(models.Model):
	conf_id = models.ForeignKey(Conference)
	papers = models.ManyToManyField(Conf_Paper,null=True,blank=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return (self.user.username+" --> "+self.conf_id.conference_name)

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	contact = models.CharField(max_length=20,null=True)
	profilepic = models.ImageField(upload_to=get_user_profile_picture_path ,null=True, blank=True)
	gender = models.CharField(max_length=10,null=True)
	regConferences = models.ManyToManyField(Registered_Conference,null=True,blank=True)

	def __unicode__(self):
		return self.user.username


class Rejected_payment(models.Model):
	conf_id = models.ForeignKey(Conference)
	user = models.ForeignKey(User)
	pic_of_dd = models.ImageField(upload_to=get_dd_path,null=True,blank=True)
	date = models.DateField()

	def __unicode__(self):
		return (self.user.username+" for "+self.conf_id.conference_name+" - "+self.date.strftime("%Y-%m-%d"))
