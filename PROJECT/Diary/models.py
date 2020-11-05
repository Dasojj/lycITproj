from django.db import models
from django.conf import settings

class Profile(models.Model):
    username = models.CharField(max_length=50, null=True)
    usermail = models.CharField(max_length=50, null=True)
    oldmail = models.CharField(max_length=50, null=True)

class BigNote(models.Model):
    creatorname = models.CharField(max_length=50, null=True)
    creationdate = models.DateField(auto_now_add=True, null=True)
    title = models.CharField(max_length=50, null=True)
    notetext = models.TextField()

class LittleNote(models.Model):
    creatorname = models.CharField(max_length=50, null=True)
    creationdate = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50, null=True)
    notetext = models.CharField(max_length=210, null=True)
    notifydate = models.DateTimeField(null=True)

class EventNote(models.Model):
    creatorname = models.CharField(max_length=50, null=True)
    creationdate = models.DateField(auto_now_add=True)
    eventdate = models.DateTimeField()
    notetext = models.CharField(max_length=210, null=True)
    eventtype = models.CharField(max_length=50, null=True)
    eventimage = models.ImageField(null=True, upload_to="images")

class MoodNote(models.Model):
    creatorname = models.CharField(max_length=50, null=True)
    creationdate = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50, null=True)
    mooddate = models.DateTimeField()
    notetext = models.CharField(max_length=210, null=True)
    eventtype = models.CharField(max_length=50, null=True)
    moodtype = models.CharField(max_length=50, null=True)