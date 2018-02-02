from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import DiscussionView, DiscussionEditView

urlpatterns = [
    path('<slug:activity_slug>/<int:page_index>/', login_required(DiscussionView.as_view()), name='discussion'),
    path('<slug:activity_slug>/<int:page_index>/Edit/',
         login_required(DiscussionEditView.as_view()),
         name='discussion_edit')
]