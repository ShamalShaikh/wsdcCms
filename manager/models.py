from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Manager(models.Model):
	user = models.OneToOneField(User)

	def  __unicode__(self):
		return self.user.username

