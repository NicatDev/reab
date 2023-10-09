from django.shortcuts import render, redirect, get_object_or_404
from meetingapp.models import *
from django.http import JsonResponse
from datetime import date,timedelta,datetime
from meetingapp.forms import Messageform,Surveyform
from django.http import HttpResponse
import json
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import login as auth_login
from meetingapp.utils import code_slug_generator

    
# Create your views here.
import calendar

def meetjoin(request):
    context = {}
    return render(request,'index.html',context)

def home(request):
    if Header.objects.all().exists():
        header = Header.objects.first()
    else:
        header = {}
    you = 'early'
    meetings = Meeting.objects.all()
    sportmen = Sportmen.objects.all()
    partners = Partners.objects.all()
    if About.objects.all().exists():
        about = About.objects.first()
    else:
        about = {}
    today = date.today()
    days_in_current_month = calendar.monthrange(today.year, today.month)[1]
    start_week = today - timedelta(days=today.weekday())
    end_week = today + timedelta(days=(7-today.weekday()))

    start_month = today - timedelta(days=today.day)
    end_month = today + timedelta(days=(days_in_current_month-today.day))
    
    day_meetings = meetings.filter(date__date=today)
    week_meetings = meetings.filter(date__date__gte=start_week,date__date__lte=end_week).exclude(date__date=today)
    month_meetings = meetings.filter(date__date__gte=start_month,date__date__lte=end_month).exclude(date__date__gte=start_week,date__date__lte=end_week)
    if meetings.filter(date__date__gte=today).exists():

        nearest_meeting = meetings.filter(date__date__gte=today).order_by('date')[0].date
        if nearest_meeting.day <= today.day:
            you = 'late'
    else:
 
        nearest_meeting = 'late'
    meetnumber = len(Meeting.objects.all())
    eagernumber = len(Eager.objects.all())
    sportmennumber = len(Sportmen.objects.all())
    
    context = {
        'header':header,
        'about':about,
        'sportmen':sportmen,
        'partners':partners,
        'day_meetings':day_meetings,
        'week_meetings':week_meetings,
        'month_meetings':month_meetings,
        'nearest_meeting':nearest_meeting,
        'you':you,
        'meetnumber':meetnumber,
        'eagernumber':eagernumber,
        'sportmennumber':sportmennumber
    }
    
    return render(request,'index-5.html',context)

def contact(request):
    if Header.objects.all().exists():
        header = Header.objects.first()
    else:
        header = {}
    meetnumber = len(Meeting.objects.all())
    eagernumber = len(Eager.objects.all())
    sportmennumber = len(Sportmen.objects.all()) 
    context = {'header':header,
        'meetnumber':meetnumber,
        'eagernumber':eagernumber,
        'sportmennumber':sportmennumber
        }
    return render(request,'contact.html',context)

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    next_page = request.GET.get('next', reverse('home'))  # Default to the home page
    return redirect(next_page)

def login(request):
  
    
    if Header.objects.all().exists():
        header = Header.objects.first()
    else:
        header = {}
    meetnumber = len(Meeting.objects.all())
    eagernumber = len(Eager.objects.all())
    sportmennumber = len(Sportmen.objects.all()) 
    
    



    context = {'header':header,
        'meetnumber':meetnumber,
        'eagernumber':eagernumber,
        'sportmennumber':sportmennumber,

        }
    return render(request,'login-register.html',context)

from django.http import JsonResponse

def message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        newmessage = Messageform(data=data)
        if newmessage.is_valid():
            newmessage.save()
        data = {'message': 'Data saved successfully'}
        return JsonResponse(data)
    else:
        return HttpResponse(status=405) 

def login_register(request):
    myaction = request.GET.get('myaction', reverse('login'))
    myresponse = {'message':'success'}

    if request.method == 'POST':
    
        data = json.loads(request.body)
    
        if myaction == '2':
            
            login_form = AuthenticationForm(request, data=data)
    
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
   
                
                return JsonResponse(myresponse)
            else:
      
                return HttpResponse(status=400) 
                # Replace 'home' with the URL of your home page
        elif myaction == '1':
            registration_form = UserCreationForm(data)
            if registration_form.is_valid():
                user = registration_form.save()
                auth_login(request, user)
                return JsonResponse(myresponse)
            else:

                
                return HttpResponse(status=400)  
        return HttpResponse(status=200) 
            # Replace 'home' with the URL of your home page
    else:
        return HttpResponse(status=405) 


def survey(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        newmessage = Surveyform(data=data)
        if newmessage.is_valid():
            newmessage.save()
        data = {'message': 'Data saved successfully'}
        return JsonResponse(data)
    else:
        return HttpResponse(status=405) 


def forgot(request):
    if Header.objects.all().exists():
        header = Header.objects.first()
    else:
        header = {}
    meetnumber = len(Meeting.objects.all())
    eagernumber = len(Eager.objects.all())
    sportmennumber = len(Sportmen.objects.all()) 
    context = {'header':header,
        'meetnumber':meetnumber,
        'eagernumber':eagernumber,
        'sportmennumber':sportmennumber
        }
    return render(request,'forgot.html',context)

def send_mail(request):
    
    data = json.loads(request.body)
    email = ''
    if validate_email(data.email):
        email = data.email
        user = User.objects.get(email = data.email)
    else:
        user = User.objects.get(username = data.email)
        email = user.email
    
    password = ForgottenPassword(user=user,forgot_password=code_slug_generator(),last_forgot=datetime.now())
    password.save()
        
    content = password.forgot_password
    
    send_mail(
            "Zehmet olmasa sifreni daxil edin. Istifade mudddeti 5 deqiqedir",
            content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False, html_message=content
    )
    return JsonResponse(data)
