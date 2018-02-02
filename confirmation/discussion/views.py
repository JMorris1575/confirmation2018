from django.shortcuts import render, redirect
from django.views import View
from activity.models import Activity, Page, Response, Choice
from django.contrib.auth.models import AnonymousUser
from config.mixins import ResponseMixin


# Create your views here.

class DiscussionView(View):
    template_name = 'discussion/discussion.html'

    def get(self, request, activity_slug=None, page_index=None):
        print('Got to the get method')
        activity = Activity.objects.get(slug=activity_slug)
        page = Page.objects.get(index=page_index)
        if not page.allowed(request.user, activity_slug, page_index):
            return redirect('summary', activity_slug)
        responses = Response.objects.filter(activity=activity, page=page)
        if len(responses) == 0:
            responses = None
        context = {'activity':activity, 'page':page, 'responses':responses}
        return render(request, self.template_name, context)

    def post(self, request, activity_slug=None, page_index=None):
        print('Got to the post method')
        activity = Activity.objects.get(slug=activity_slug)
        page = Page.objects.get(index=page_index)
        entry = request.POST['entry'].strip()
        if page.discussion_type == 'OP' or page.discussion_type == 'SA':
            user = request.user
        else:
            user = AnonymousUser
        if len(entry) != 0:
            response = Response(user=user, activity=activity, page=page,
                                essay=entry, completed=True)
            response.save()
        return redirect('discussion', activity_slug, page_index)
