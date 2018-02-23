from django.shortcuts import render
from django.views import View
from django.core.exceptions import PermissionDenied
from config.utilities import get_group_names
from .models import DevelopingActivity
from activity.models import Activity, Page

from config.utilities import PageMixin

# Create your views here.


class DevActivitiesListView(View):
    template_name = 'development/activity_list.html'

    def get(self, request):
        group_names = get_group_names(request.user)
        if 'Administrator' in group_names or 'Supervisor' in group_names or 'Team' in group_names:
            dev_activities = DevelopingActivity.objects.all()
            return render(request, self.template_name, {'group_names': group_names,
                                                        'dev_activities': dev_activities})
        else:
            raise PermissionDenied


class DevSummaryView(View):
    template_name = 'development/dev_summary.html'

    def get(self, request, activity_slug=None):
        group_names = get_group_names(request.user)
        if 'Administrator' in group_names or 'Supervisor' in group_names or 'Team' in group_names:
            activity = Activity.objects.get(slug=activity_slug)
            activity_dev = DevelopingActivity.objects.get(activity=activity)
            pages = Page.objects.filter(activity=activity)
            return render(request, self.template_name, {'group_names': group_names,
                                                        'activity': activity,
                                                        'pages': pages,
                                                        'activity_dev': activity_dev,
                                                        'can_edit': activity_dev.can_edit(request.user)})
        else:
            raise PermissionDenied


