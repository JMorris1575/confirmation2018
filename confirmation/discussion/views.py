from django.shortcuts import render, redirect
from django.views import View
from activity.models import Activity, Page, Response, Choice
from django.contrib.auth.models import AnonymousUser
from config.mixins import ResponseMixin


# Create your views here.

class DiscussionView(ResponseMixin, View):
    template_name = 'discussion/discussion.html'

    def get(self, request, activity_slug=None, page_index=None):
        activity, page, responses, context = self.get_response_info(request.user, activity_slug, page_index)
        if not page.allowed(request.user, activity_slug, page_index):
            return redirect('summary', activity_slug)
        context['responses'] = responses                        # get_response_info only returns a single response
        return render(request, self.template_name, context)

    def post(self, request, activity_slug=None, page_index=None):
        activity, page, responses, context = self.get_response_info(request.user, activity_slug, page_index)
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


class DiscussionEditView(View):
    pass