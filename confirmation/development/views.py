from django.shortcuts import render
from django.views import View

from config.mixins import PageMixin

# Create your views here.


class DevActivitiesListView(View):
    template_name = 'development/activity_list.html'

    def get(self, request):
        group_names = PageMixin.get_group_names(request.user)
        return render(request, self.template_name, {'group_names': group_names})

