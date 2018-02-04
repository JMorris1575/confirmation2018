from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import DiscussionView, DiscussionEditView, DiscussionDeleteView

urlpatterns = [
    path('<slug:activity_slug>/<int:page_index>/', login_required(DiscussionView.as_view()), name='discussion'),
    path('<slug:activity_slug>/<int:page_index>/<int:response_pk>/Edit/',
         login_required(DiscussionEditView.as_view()),
         name='discussion_edit'),
    path('<slug:activity_slug>/<int:page_index>/<int:response_pk>/Delete/',
         login_required(DiscussionDeleteView.as_view()),
         name='discussion_delete'),
]