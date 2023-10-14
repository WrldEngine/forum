from django.contrib import admin
from .models import ForumUser, Questions, Answers, Posts

# Register your models here.
admin.site.register(ForumUser)
admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(Posts)