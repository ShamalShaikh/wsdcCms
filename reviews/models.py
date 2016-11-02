from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from conference.models import Conf_Paper, Conference
# Create your models here.

class Reviewer(models.Model):
	user = models.ForeignKey(User)
	papers = models.ManyToManyField(Conf_Paper, null=True, blank=True)

	def __str__(self):
		return str(self.user)

class Questions(models.Model):
	question = models.TextField()
	conference = models.ForeignKey(Conference, default = 1)

	def __str__(self):
		return self.question

class Answers(models.Model):
	question = models.ForeignKey(Questions)
	answer = models.TextField()
	reviewer = models.ForeignKey(Reviewer)

	def __str__(self):
		return (str(self.question)+' ' + str(self.reviewer))