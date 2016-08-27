from django.db import models

def conference_directory_path(instance, filename):
    return 'uploads/{0}'.format(filename)
    #return 'uploads/{0}/{1}'.format(Conference.objects.get(cid__exact=instance.cid).__unicode__, filename)

class User(models.Model):
    uid = models.AutoField(primary_key = True)
    uname = models.CharField(max_length = 20)
    emailId = models.CharField(max_length = 35)
    cellNo = models.IntegerField()
    permissions = models.IntegerField()
    password = models.CharField(max_length = 16)

class Conference(models.Model):
    cid = models.AutoField(primary_key = True)
    conferenceName = models.CharField(max_length = 100)
    mid = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    STATUS = (
        ('U' , 'Upcoming'),
        ('P' , 'Previous'),
    )
    status = models.CharField(max_length = 1 , choices = STATUS )
    alias = models.CharField(max_length = 10)
    description = models.CharField(max_length = 100)

class Paper(models.Model):
    paperid = models.AutoField(primary_key = True)
    cid = models.ForeignKey(Conference, on_delete=models.CASCADE)
    pname = models.CharField(max_length = 100)
    description = models.CharField(max_length = 100)
    submissionDate = models.DateField()
    approved = models.BooleanField(default=False)
    paperFile = models.FileField(upload_to=conference_directory_path)

class Page(models.Model):
    pid = models.AutoField(primary_key = True)
    cid = models.ForeignKey(Conference, on_delete = models.CASCADE)
    pageName = models.CharField(max_length = 20)
    content = models.CharField(max_length = 1000)
