from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Activity, Page, Response

# Create your views here.

class WelcomeView(View):
    template_name = 'activity/welcome.html'

    def get(self, request):
        activities = Activity.objects.all()
        user_stats = {}
        for activity in activities:
            pages = Page.objects.filter(activity=activity)
            page_count = len(pages)
            completed = len(Response.objects.filter(user=request.user, activity=activity))
            if page_count != 0:
                user_stats[activity.slug] = completed/page_count * 100
            else:
                user_stats[activity.slug] = -1

        return render(request, self.template_name, {'activities':activities, 'stats':user_stats})

    def post(self, request):
        return render(request, self.template_name)


class SummaryView(View):
    template_name = 'activity/summary.html'

    def get(self, request, activity_slug):
        activity = Activity.objects.get(slug=activity_slug)
        return render(request, self.template_name, {'activity': activity,
                                                    'pages':Page.objects.filter(activity=activity.pk)})
