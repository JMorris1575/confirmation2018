from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

app_name = 'user'
urlpatterns = [
    path('', RedirectView.as_view(url='/user/login/')), #pattern_name='login', permanent=False)),
    path('login/', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'template_name': 'registration/login.html'}, name='logout')

]
