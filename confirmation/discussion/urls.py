from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import DiscussionView

urlpatterns = [
    path('<slug:activity_slug>/<int:page_index>/', login_required(DiscussionView.as_view()), name='discussion'),

]