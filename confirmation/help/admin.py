from django.contrib import admin
from .models import HelpCategory, HelpPage

# Register your models here.

admin.site.register(HelpCategory)
admin.site.register(HelpPage)