from django.urls import path, include
from django.views.generic import RedirectView
from .views import EmailView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', RedirectView.as_view(url='mail/send/')),
    path('send/', login_required(EmailView.as_view()), name='send_email')
]
