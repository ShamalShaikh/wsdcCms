from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.core.exceptions import ValidationError

def conference_directory_path(instance, filename):
    return 'uploads/{0}'.format(filename)
    #return 'uploads/{0}/{1}'.format(Conference.objects.get(cid__exact=instance.cid).__unicode__, filename)

#class User(models.Model):
#    uid = models.AutoField(primary_key = True)
#    uname = models.CharField(max_length = 20)
#    emailId = models.CharField(max_length = 35)
#    cellNo = models.IntegerField()
#    permissions = models.IntegerField()
#    password = models.CharField(max_length = 16)

class Conference(models.Model):
    cid = models.AutoField(primary_key = True)
    conferenceName = models.CharField(max_length = 100)
    mid = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    startDate = models.DateField()
    endDate = models.DateField()

    STATUS = (
        ('U' , 'Upcoming'),
        ('P' , 'Previous'),
    )
    status = models.CharField(max_length = 1 , choices = STATUS )
    alias = models.CharField(max_length = 10)
    description = models.CharField(max_length = 100)

    def __str__(self):
        return self.alias

@receiver(post_save, sender=Conference)
def create_conference(sender, instance, created, **kwargs):
    if created:
        tempuser = User.objects.get(username=instance.mid)
        print(tempuser.username)
        tempuser.profile.conferenceId = instance.cid
        tempuser.save()




class Paper(models.Model):
    paperid = models.AutoField(primary_key = True)
    cid = models.ForeignKey(Conference)
    uid = models.ForeignKey(User)

    pname = models.CharField(max_length = 100)
    description = models.CharField(max_length = 100)
    submissionDate = models.DateField()
    approved = models.BooleanField(default=False)

    def validate(value):
        import os
        ext = os.path.splitext(value.name)[1]
        valid_extentions = ['.pdf','.doc','.docx']
        if not ext in valid_extentions:
            raise ValidationError(u'File type is not supported')

    paperFile = models.FileField(upload_to=conference_directory_path, validators=[validate])



    def __str__(self):
        return str(self.paperid)

class Page(models.Model):
    pid = models.AutoField(primary_key = True)
    cid = models.ForeignKey(Conference, on_delete = models.CASCADE)
    pageUrl = models.CharField(max_length = 20)
    pageName = models.CharField(max_length = 50)
    content = models.CharField(max_length = 1000)

    def __str__(self):
        return self.pageUrl

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, blank=True)
    conferenceId = models.IntegerField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
