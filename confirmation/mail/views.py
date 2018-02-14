from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User, Group
from config.mixins import PageMixin

# Create your views here.


class EmailView(View):
    template_name = 'mail/send-mail.html'

    def get(self, request):
        if request.user.is_authenticated:
            group_names = PageMixin.get_group_names(self, request.user)
        else:
            group_names = None
        supervisors = Group.objects.get(name="Supervisor").user_set.all().order_by('last_name')
        team_members = Group.objects.get(name="Team").user_set.all().order_by('last_name')
        candidates = Group.objects.get(name="Candidate").user_set.all().order_by('last_name')
        context = {'group_names': group_names,
                   'supervisors': supervisors,
                   'team_members': team_members,
                   'candidates': candidates}

        return render(request, self.template_name, context)
