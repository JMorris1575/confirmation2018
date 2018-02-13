from django.urls import path, include
from django.views.generic import RedirectView
from .views import EmailView

urlpatterns = [
    path('', RedirectView.as_view(url='mail/send/')),
    path('send/', EmailView.as_view(), name='send_email')
]
