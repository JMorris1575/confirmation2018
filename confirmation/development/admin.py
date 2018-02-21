from django.contrib import admin
from .models import DevelopingActivity, Developer, Comment

# Register your models here.

admin.site.register(DevelopingActivity)
admin.site.register(Developer)
admin.site.register(Comment)
