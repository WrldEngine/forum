from django.contrib import admin
from .models import ForumUser, Questions, Answers

# Register your models here.
admin.site.register(ForumUser)
admin.site.register(Questions)
admin.site.register(Answers)