from django.shortcuts import render, redirect
from django.views import View
from activity.models import Activity, Page, Response, Choice
from django.contrib.auth.models import User
from config.mixins import PageMixin


# Create your views here.

class DiscussionView(PageMixin, View):
    template_name = 'discussion/discussion.html'

    def get(self, request, activity_slug=None, page_index=None):
        activity, page, user_responses, context = self.get_response_info(request.user, activity_slug, page_index)
        if not page.allowed(request.user, activity_slug, page_index):
            return redirect('summary', activity_slug)
        context['responses'] = Response.objects.filter(activity=activity, page=page)   # get all the page's responses
        return render(request, self.template_name, context)

    def post(self, request, activity_slug=None, page_index=None):
        activity, page, responses, context = self.get_response_info(request.user, activity_slug, page_index)
        entry = request.POST['entry'].strip()
        if page.discussion_type == 'OP' or page.discussion_type == 'SA':
            user = request.user
        else:
            user = User.objects.get(username='Unknown')
        if len(entry) != 0:
            response = Response(user=user, activity=activity, page=page,
                                essay=entry, completed=True)
            response.save()
        return redirect('discussion', activity_slug, page_index)


class DiscussionEditView(PageMixin, View):

    def get(self, request, activity_slug=None, page_index=None, response_pk=None):
        activity, page, responses, context = self.get_response_info(request.user, activity_slug, page_index)
        response = Response.objects.get(pk=response_pk)
        context['response'] = response
        return render(request, 'discussion/discussion_edit.html', context)

    def post(self, request, activity_slug=None, page_index=None, response_pk=None):
        if request.POST['button'] == 'OK':
            response = Response.objects.get(pk=response_pk)
            response.essay = request.POST['entry']
            response.save()
        return redirect('discussion', activity_slug, page_index)


class DiscussionDeleteView(PageMixin, View):

    def get(self, request, activity_slug=None, page_index=None, response_pk=None):
        activity, page, responses, context = self.get_response_info(request.user, activity_slug, page_index)
        response = Response.objects.get(pk=response_pk)
        context['response'] = response
        return render(request, 'discussion/discussion_delete.html', context)

    def post(self, request, activity_slug=None, page_index=None, response_pk=None):
        activity, page, responses, context = self.get_response_info(request.user, activity_slug, page_index)
        print('DiscussionDeleteView request.POST = ', request.POST)
        if request.POST['user-choice'] == 'Delete':
            response = responses.get(pk=response_pk)
            response.delete()

        return redirect('discussion', activity_slug, page_index)
