from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('contact',contact,name='contact'),
    path('message',message,name='message'),
    path('login_register',login_register,name='login_register'),
    path('survey',survey,name='survey'),

    path('login/',login,name='login'),
    path('forgot',forgot,name='forgot'),
    path('meetjoin',meetjoin,name='meetjoin'),
    path('logout/',logout_view, name='logout'),
]
