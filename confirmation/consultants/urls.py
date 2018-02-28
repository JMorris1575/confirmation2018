from django.urls import path
from django.views.generic import RedirectView
from .views import CritiqueView, EditCritiqueView, ToggleCritiquesView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', CritiqueView.as_view(), name='save_critique'),
    path('Edit/<int:pk>/', EditCritiqueView.as_view(), name='critique_edit'),
    path('toggle_critiques/', ToggleCritiquesView.as_view(), name='toggle_critiques'),
]