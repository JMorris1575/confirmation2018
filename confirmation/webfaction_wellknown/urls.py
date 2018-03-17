from django.urls import path, include

from . import views


urlpatterns = [
    path('<str:challenge_filename>', views.data, name='data'),
]