from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Activity, Page

# Create your views here.

class WelcomeView(View):
    template_name = 'activity/welcome.html'

    def get(self, request):
        return render(request, self.template_name, {'activities':Activity.objects.all()})

    def post(self, request):
        return render(request, self.template_name)


class SummaryView(View):
    template_name = 'activity/summary.html'

    def get(self, request, activity_slug):
        activity = Activity.objects.get(slug=activity_slug)
        return render(request, self.template_name, {'activity': activity,
                                                    'pages':Page.objects.filter(activity=activity.pk)})
