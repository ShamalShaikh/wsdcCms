from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from conference.models import *


def get_user_profile_picture_path(instance,filename):
    return 'userprofile/{0}'.format(filename)

class Registered_Conference(models.Model):
	conf_id = models.ForeignKey(Conference)
	papers = models.ManyToManyField(Conf_Paper,null=True,blank=True)
	user = models.OneToOneField(User)

	def __unicode__(self):
		return (self.user+" --> "+self.conf_id)

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	contact = models.CharField(max_length=20,null=True)
	profilepic = models.ImageField(upload_to=get_user_profile_picture_path ,null=True, blank=True)
	gender = models.CharField(max_length=10,null=True)
	regConferences = models.ManyToManyField(Registered_Conference,null=True,blank=True)

	def __unicode__(self):
		return self.user.username


	


