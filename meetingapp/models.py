from django.db import models
from django.contrib.auth import get_user, get_user_model
from meetingapp.utils import *
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

class Partners(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=120)
    def __str__(self):
        return self.title
    
class About(models.Model):
    bigimage = models.ImageField(verbose_name='630-522')
    smallimage = models.ImageField(verbose_name='344-285')
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=190,verbose_name='180-190 herf max content')
    content2 = models.CharField(max_length=120,verbose_name='110-120 herf max content')
    
    def __str__(self):
        return "Haqqinda bolmesi"
    
    def save(self, *args, **kwargs):
        self.pk = 1  
        super(About, self).save(*args, **kwargs)
    
class Sportmen(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='owner')
    field = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=120)
    titul = models.CharField(max_length=1200)
    is_active = models.BooleanField(default=False)
    image = models.ImageField(null=True,blank=True)
    personal_information = models.CharField(max_length=1200,null=True,blank=True)
    
    def __str__(self):
        return self.user.first_name + self.user.last_name + self.field
    
class Message(models.Model):
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    subject = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    message = models.CharField(max_length=120)
    
    def __str__(self):
        return self.name

class Header(models.Model):
    minititle1 = models.CharField(max_length=120)
    title1 = models.CharField(max_length=200)
    minititle2 = models.CharField(max_length=120)
    title2 = models.CharField(max_length=200)
    minititle3 = models.CharField(max_length=120)
    title3 = models.CharField(max_length=200)
    image1 = models.ImageField()
    image2 = models.ImageField()
    image3 = models.ImageField()
    
    def save(self, *args, **kwargs):
        self.pk = 1  
        super(Header, self).save(*args, **kwargs)
    
    def __str__(self):
        return 'Header 3 slide'
    
    
class Eager(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    field = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=120)
    is_blocked = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
class ForgottenPassword(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='forgot')
    forgot_password = models.CharField(max_length=120,null=True,blank=True)
    last_forgot = models.DateTimeField(null=True,blank=True)


class Meeting(models.Model):
    title = models.CharField(max_length=120,null=True,blank=True)
    content = models.CharField(max_length=1200,null=True,blank=True)
    content2 = models.CharField(max_length=1200,null=True,blank=True)
    meeter = models.ManyToManyField(User,related_name='meetings')
    meetingowner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='adventures')
    date = models.DateTimeField()
    time = models.CharField(max_length=1200,verbose_name='saat like 10:00 or 10:00-11:00')
    sportfield = models.CharField(max_length=1200)
    location = models.CharField(max_length=1200)
    meeting_id = models.TextField(null=True,blank=True)
    finished = models.BooleanField(default=False)
    meeting_duration = models.CharField(max_length=120,verbose_name='gorus vaxti')
    
    def __str__(self):
        return self.meetingowner.username
    

class Survey(models.Model):
    name = models.CharField(max_length=1200)
    
    def __str__(self):
        return self.name
