from django.contrib import admin
from .models import CustomUser, Test, Question, Result

admin.site.register(CustomUser)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Result)
