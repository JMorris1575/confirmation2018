from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

from .views import DevActivitiesListView, DevSummaryView

urlpatterns = [
    path('', RedirectView.as_view(url='development/activities/')),
    path('activities/', login_required(DevActivitiesListView.as_view()), name='dev_activity_list'),
    path('<slug:activity_slug>/', login_required(DevSummaryView.as_view()), name='dev_summary'),
    
]