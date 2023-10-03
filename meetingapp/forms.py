from django import forms
from .models import *

class Messageform(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['name','email','message','phone','subject']
    
        
    def __init__(self,*args,**kvargs):
        super(Messageform,self).__init__(*args,**kvargs)
        

class Surveyform(forms.ModelForm):

    class Meta:
        model = Survey
        fields = ['name']
    
    def __init__(self,*args,**kvargs):
        super(Surveyform,self).__init__(*args,**kvargs)