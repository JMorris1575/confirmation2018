from django.shortcuts import render, redirect
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
        responses = Response.objects.filter(user=request.user, activity=activity.pk, page=page.pk)
        if len(responses) != 0:
            response = responses[0]
        else:
            response = None
        context = {'activity': activity, 'page': page, 'response': response}
        if page.page_type == 'IN':
            self.template_name = 'activity/instructions.html'
        elif page.page_type == 'ES':
            self.template_name = 'activity/essay.html'
        return render(request, self.template_name, context)

    def post(self, request, activity_slug=None, page_index=None):
        activity = Activity.objects.get(slug=activity_slug)
        page = Page.objects.get(activity=activity.pk, index=page_index)
        if page.page_type == 'IN':
            response = Response(user=request.user, activity=activity, page=page, completed=True)
            response.save()
        elif page.page_type == 'ES':
            response = Response(user=request.user, activity=activity, page=page,
                                essay=request.POST['essay'].strip(), completed=True)
            response.save()
        return redirect('summary', activity_slug )


class PageEditView(View):

    def get(self, request, activity_slug=None, page_index=None):
        activity = Activity.objects.get(slug=activity_slug)
        page = Page.objects.get(index=page_index)
        response = Response.objects.get(user=request.user, activity=activity, page=page)
        context = {'activity': activity, 'page': page, 'response': response}
        if page.page_type == 'ES':
            self.template_name = 'activity/essay_edit.html'

        return render(request, self.template_name, context)



class PageDeleteView(View):
    pass