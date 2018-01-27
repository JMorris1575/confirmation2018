from django.urls import path
from django.views.generic import RedirectView
from .views import WelcomeView, SummaryView, PageView, PageEditView, PageDeleteView
from django.contrib.auth.decorators import login_required
from django.contrib import admin

urlpatterns = [
    path('', RedirectView.as_view(url='/activity/welcome/')), #pattern_name='welcome', permanent=False)),
    path('welcome/', login_required(WelcomeView.as_view()), name='welcome'),
    path('<slug:activity_slug>/summary/', login_required(SummaryView.as_view()), name='summary'),
    path('<slug:activity_slug>/<int:page_index>/', login_required(PageView.as_view()), name='page'),
    path('<slug:activity_slug>/<int:page_index>/edit', login_required(PageEditView.as_view()), name='edit'),
    path('<slug:activity_slug>/<int:page_index>/delete', login_required(PageDeleteView.as_view()), name='delete'),
]
