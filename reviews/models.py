from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from conference.models import Conf_Paper, Conference
# Create your models here.

class Reviewer(models.Model):
	user = models.ForeignKey(User)
	papers = models.ManyToManyField(Conf_Paper, null=True, blank=True)
	conference = models.ForeignKey(Conference,null=True)

	def __str__(self):
		return str(self.user)

class Questions(models.Model):
	question = models.TextField()
	conference = models.ForeignKey(Conference)
	que_type = models.IntegerField(default=0)

	def __str__(self):
		return self.question

class Answers(models.Model):
	question = models.ForeignKey(Questions)
	answer = models.TextField()
	marks = models.IntegerField(default=0)
	reviewer = models.ForeignKey(Reviewer)
	paper = models.ForeignKey(Conf_Paper)

	def __str__(self):
		return (str(self.question)+' - ' + str(self.reviewer)+' - '+str(self.paper))

class Remarks(models.Model):
	answer = models.TextField()
	reviewer = models.ForeignKey(Reviewer)
	paper = models.ForeignKey(Conf_Paper)

	def __str__(self):
		return ("Remark " + str(self.reviewer))

class AssignedPaperStatus(models.Model):
	paper = models.ForeignKey(Conf_Paper)
	reviewer = models.ForeignKey(Reviewer)
	reviewStatus = models.IntegerField(default=0)
	# 0 - assigned , 1 - submitted

	def __str__(self):
		return (self.paper.papername+"-"+self.reviewer.user.username)