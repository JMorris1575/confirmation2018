from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Activity, Page, Response

import datetime

# Create your views here.

class WelcomeView(View):
    template_name = 'activity/welcome.html'

    def get(self, request):
        activities = Activity.objects.filter(publish_date__lte=datetime.date.today(),
                                             closing_date__gt=datetime.date.today(),
                                             visible=True)
        data = []
        for activity in activities:
            pages = Page.objects.filter(activity=activity)
            page_count = len(pages)
            completed = len(Response.objects.filter(user=request.user, activity=activity, completed=True))
            if page_count != 0:
                percent_completed = completed/page_count * 100
                if percent_completed < 100:
                    msg = '{:.1f}'.format(percent_completed) + '% Complete'
                else:
                    msg = 'Finished!'
            else:
                msg = 'Not Yet Available'
            data.append((activity, msg))

        return render(request, self.template_name, {'data': data})

    def post(self, request):
        return render(request, self.template_name)


class SummaryView(View):
    template_name = 'activity/summary.html'

    def get(self, request, activity_slug):
        activity = Activity.objects.get(slug=activity_slug)
        pages = Page.objects.filter(activity=activity.pk)
        responses = Response.objects.filter(user=request.user, activity=activity.pk)
        data = []
        changing_msg = 'Up next...'
        for page in pages:
            if responses.filter(page=page.pk):
                data.append((page, 'Completed'))
            else:
                data.append((page, changing_msg))
                changing_msg = 'Pending'
        return render(request, self.template_name, {'activity': activity,
                                                    'data': data})


class PageView(View):

    def get(self, request, activity_slug, page_index):
        activity = Activity.objects.get(slug=activity_slug)
        page = Page.objects.get(activity=activity.pk, index=page_index)
        response = Response.objects.filter(user=request.user, activity=activity.pk, page=page.pk)
        if page.page_type == 'IN':
            self.template_name = 'activity/instructions.html'
            context = self.get_instruction_context(request, activity, page, response)
        return render(request, self.template_name, context)

    def get_instruction_context(self, request, activity, page, response):
        context = {}
        context['activity'] = activity
        context['page'] = page
        context['response'] = response
        return context