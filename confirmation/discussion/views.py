from django.shortcuts import render
from django.views import View
from activity.models import Activity, Page, Response, Choice
from config.mixins import ResponseMixin


# Create your views here.

class DiscussionView(View):
    template_name = 'discussion/discussion.html'

    def get(self, request, activity_slug=None, page_index=None):
        activity = Activity.objects.get(slug=activity_slug)
        page = Page.objects.get(index=page_index)
        responses = Response.objects.filter(user=request.user, activity=activity, page=page)
        if len(responses) == 0:
            responses = None
        context = {'activity':activity, 'page':page, 'responses':responses}
        return render(request, self.template_name, context)