from django.urls import path
from django.views.generic import RedirectView
from .views import CritiqueView, ToggleCritiquesView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', CritiqueView.as_view(), name='save_critique'),
    path('suggestions/toggle_critiques', ToggleCritiquesView.as_view(), name='toggle_critiques'),
]