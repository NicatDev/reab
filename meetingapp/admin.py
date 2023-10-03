from django.contrib import admin
from meetingapp.models import Meeting,Eager,Sportmen,Partners,About,Header,Message,Survey
from django.contrib.auth import get_user_model

User = get_user_model()

from django.db import models
# class MyModelAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.TextField: {'widget': CKEditorWidget(config_name='default')},
#     }
# admin.site.register(HomeHeader)
admin.site.register(Message)
admin.site.register(Meeting)
admin.site.register(Sportmen)
admin.site.register(Partners)
admin.site.register(Eager)
admin.site.register(About)
admin.site.register(Header)
admin.site.register(Survey)

