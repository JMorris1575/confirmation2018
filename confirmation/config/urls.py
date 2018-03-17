"""confirmation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

from .views import HelpView

urlpatterns = [
    path('', RedirectView.as_view(url='user/login/')),
    path('user/', include('user.urls'), name='dj-auth'),
    path('help/', include('help.urls')),
    path('activity/', include('activity.urls')),
    path('admin/', admin.site.urls),
    path('discussion/', include('discussion.urls')),
    path('email/', include('mail.urls')),
    path('develop/', include('development.urls')),
    path('suggestions/', include('consultants.urls')),
    path('.well-known/', include('webfaction_wellknown.urls')),
]

admin.site.site_header = 'St. Basil Confirmation 2018 Admin'
admin.site.site_title = 'Confirmation2018 Site Admin'