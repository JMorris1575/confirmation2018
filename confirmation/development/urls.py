from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

from .views import DevActivitiesListView

urlpatterns = [
    path('/', RedirectView.as_view(url='development/activities/')),
    path('/activities/', DevActivitiesListView.as_view(), name='dev_activity_list')
    
]