from django.shortcuts import render, redirect, get_object_or_404
from meetingapp.models import *
from django.http import JsonResponse
from datetime import date,timedelta,datetime
from meetingapp.forms import Messageform,Surveyform,CustomUserCreationForm
from django.http import HttpResponse
import json
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import login as auth_login
from meetingapp.utils import code_slug_generator,validateEmail
from django.contrib.auth.decorators import login_required
import pytz
# Create your views here.
import calendar

def meetjoin(request,meet):
    mymeet = Meeting.objects.get(id=meet)
    zoom_url = mymeet.meeting_id
    url_parts = zoom_url.split('/')
   
    if len(url_parts) < 5:
        return JsonResponse({"error": "Invalid Zoom URL"})

    # Extract the meeting ID and password

    password_part = url_parts[-1]
    meeting_id = url_parts[-1].split('?')[0]
    password_parts = password_part.split('=')
    if len(password_parts) < 2:
        return JsonResponse({"error": "Invalid Zoom URL"})
    
    meeting_pwd = password_parts[1].split('.')[0]
    print(meeting_id,meeting_pwd)
    context = {
        'meeting_id':meeting_id,
        'meeting_pwd':meeting_pwd
    }
    return render(request,'index.html',context)


@login_required
def speaker(request):

    
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
   
    return render(request,'speaker.html',context)

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
    now = datetime.now(pytz.utc)
    day_meetings = meetings.filter(date__date=today)
    week_meetings = meetings.filter(date__date__gte=datetime.now(),date__date__lte=end_week).exclude(date__date=today)
    month_meetings = meetings.filter(date__date__gte=datetime.now(),date__date__lte=end_month).exclude(date__date__gte=datetime.now(),date__date__lte=end_week)

    if meetings.filter(date__gte=datetime.now()).exists():
        nearest_meeting = meetings.filter(date__gte=datetime.now()).order_by('date')[0].date
        print(nearest_meeting,'nearest_meeting')
        you = 'late'
    else:

        nearest_meeting = 'late'
    meetnumber = len(Meeting.objects.all())
    eagernumber = len(Eager.objects.all())
    sportmennumber = len(Sportmen.objects.all())

    print(now,'-now',datetime.now(),'datetime.now')
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

def wishlist(request):
    if request.method == 'POST':
        
        if not request.user.is_authenticated:
            return HttpResponse(status=403) 
        data2 = {'message': 'Data saved successfully'}
        
        data = json.loads(request.body)
        user = User.objects.get(id=data.get('user'))
      
        if Meeting.objects.filter(id=data.get('id')).exists():
            meeting = Meeting.objects.get(id=data.get('id'))
        else:
            return HttpResponse(status=403) 
        if meeting in user.meetings.all():
            user.meetings.remove(meeting)
            print('removed')
            return JsonResponse(data2,status=201)
        
        else:
            user.meetings.add(meeting)
            print('added')
            return JsonResponse(data2,status=200)
    else:
        return HttpResponse(status=405) 

def login_register(request):
    myaction = request.GET.get('myaction', reverse('login'))
    myresponse = {'message':'success'}

    if request.method == 'POST':
    
        data = json.loads(request.body)
        print(data)
        if myaction == '2':
            
            login_form = AuthenticationForm(request, data=data)
            
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                
                
                return JsonResponse(myresponse)
            else:
                print(login_form.errors)
                return HttpResponse(status=400) 
                # Replace 'home' with the URL of your home page
        elif myaction == '1':
            registration_form = CustomUserCreationForm(data)
            phone_number = data.pop('phone_number')
            print(data,phone_number)
            if registration_form.is_valid():
                user = registration_form.save()
                eager = Eager(user=user,phone_number=phone_number)
                eager.save()
                auth_login(request, user)
                return JsonResponse(myresponse)
            else:
                print(registration_form.errors)
                
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


def change_password(request):
    error_data = {
        'error': 'Bad Request',
        'message': 'Wrong username or email'
    }
    data = json.loads(request.body)
    email = data.get('email')
    if data.get('pass') != data.get('confirmpass'):
        return JsonResponse(error_data,status=401)
    password = data.get('pass')
    if User.objects.filter(email = email).exists():
        user = User.objects.get(email = email)
    elif User.objects.filter(username = email).exists():
        user = User.objects.get(username = email)
    else:
        return JsonResponse(error_data,status=404)
    user.set_password(password)
    user.save()
    return JsonResponse({'message':True},status=200)

def check_password(request):
    error_data = {
        'error': 'Bad Request',
        'message': 'Wrong username or email'
    }
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('pass')
    if User.objects.filter(email = email).exists():
        user = User.objects.get(email = email)
    elif User.objects.filter(username = email).exists():
        user = User.objects.get(username = email)
    else:
        return JsonResponse(error_data,status=404)
    if user.forgot.forgot_password == password:
        
        return JsonResponse({'message':True})
    else:
        print(user.forgot.forgot_password,password)
        return JsonResponse(error_data,status=402)

    
def sendMail(request):
    
    error_data = {
        'error': 'Bad Request',
        'message': 'Wrong username or email'
    }
    
    data = json.loads(request.body)
    
    email = ''
    print(data)
    if validateEmail(data.get('email')):
        print('emaildir')
        email = data.get('email')
        if User.objects.filter(email=data.get('email')).exists():
            user = User.objects.get(email = data.get('email'))
            print('user var')
        else:
            print('email user yoxdur')
            return JsonResponse(status=403)
    else:
        print('usernamdir')
        if User.objects.filter(username = data.get('email')).exists():
            print('user var')
            user = User.objects.get(username = data.get('email'))
            email = user.email
        else:
            print('username user yoxdur')
            response = JsonResponse(error_data)
            response.status_code = 403
            return response
    if ForgottenPassword.objects.filter(user=user).exists():
        password = ForgottenPassword.objects.get(user=user)
        password.forgot_password = code_slug_generator()
        password.last_forgot = datetime.now()
        password.save()
    else:
        password = ForgottenPassword(user=user,forgot_password=code_slug_generator(),last_forgot=datetime.now())
        password.save() 
    content = password.forgot_password

    send_mail(
            "Zehmet olmasa sifreni daxil edin. Istifade mudddeti 5 deqiqedir",
            content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False, 
            html_message=content
    )
    
    return JsonResponse({'message':True})
