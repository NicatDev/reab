from django.shortcuts import render, redirect, get_object_or_404
from meetingapp.models import *
from django.db.models import Q,F,FloatField,Count
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count
from datetime import date,timedelta
from meetingapp.forms import Messageform,Surveyform
from django.http import HttpResponse
import json
# Create your views here.
import calendar
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
        'sportmennumber':sportmennumber
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
