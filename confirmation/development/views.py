from django.shortcuts import render
from django.views import View
from django.core.exceptions import PermissionDenied
from config.utilities import get_group_names

from config.utilities import PageMixin

# Create your views here.


class DevActivitiesListView(View):
    template_name = 'development/activity_list.html'

    def get(self, request):
        group_names = get_group_names(request.user)
        if 'Administrator' in group_names or 'Supervisor' in group_names or 'Team' in group_names:
            return render(request, self.template_name, {'group_names': group_names})
        else:
            raise PermissionDenied
