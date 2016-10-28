from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from conference.models import *
from login_auth.models import *
from reviews.models import Reviewer

class Manager(models.Model):
	user = models.OneToOneField(User)

	def  __unicode__(self):
		return user.username

class Paper_assign(models.Model):
	manager = models.ForeignKey(Manager)
	reviewers = models.ManyToManyField(Reviewer)
	paper = models.ForeignKey(Conf_Paper)

	def  __unicode__(self):
		return (manager.user.username+" "+paper.papername)
