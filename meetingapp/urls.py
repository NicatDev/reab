from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('contact',contact,name='contact'),
    path('message',message,name='message'),
    path('survey',survey,name='survey'),
    path('login',login,name='login'),
    path('forgot',forgot,name='forgot'),
 ]
