from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

from .views import HelpView

urlpatterns = [
    path('', RedirectView.as_view(url='help/index/')),
    path('<str:category_name>/', HelpView.as_view(), name='help_page'),
    path('<str:category_name>/<int:page_number>/', HelpView.as_view(), name='numbered_help_page'),
]