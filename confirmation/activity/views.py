from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Activity

# Create your views here.

class WelcomeView(View):
    template_name = 'activity/welcome.html'

    def get(self, request):
        return render(request, self.template_name, {'activities':Activity.objects.all()})

    def post(self, request):
        return render(request, self.template_name)