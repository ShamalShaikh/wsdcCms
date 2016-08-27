from django.db import models

class Users(models.Model):
    uid = models.AutoField(primary_key = True)
    uname = models.CharField(max_length = 20)
    emailId = models.CharField(max_length = 35)
    cellNo = models.IntegerField()
    permissions = models.IntegerField()
    password = models.CharField(max_length = 16)

class Conference(models.Model)
    cid = models.AutoField(primary_key = True)
    conferenceName = models.CharField(max_length = 100)
    mid = models.ForeignKey(Users, on_delete=models.CASCADE)
    date = models.DateField()
    STATUS (
        ('U' = 'Upcoming'),
        ('P' = 'Previous'),
    )
    status = models.CharField(max_length = 1 , choices = STATUS )
    alias = models.CharField(max_length = 10)

class papers(models.Model)
    pid = models.AutoField(primary_key = True)
    pname = models.CharField(max_length = 100)
    description = models.CharField(max_length = 100)
    submissionDate = models.DateField()
    approved = models.BooleanField(default=False)
    #p_link =models.

class page(models.Model):
    pid = models.AutoField(primary_key = True)
    cid = models.ForeignKey(Conf, on_delete = models.CASCADE)
    pageName = models.CharField(max_length = 20)
    content = models.CharField(max_length = 1000)
