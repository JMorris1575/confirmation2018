from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied

from config.utilities import get_group_names
from config.settings.base import get_secret
from config.utilities import get_group_names, get_response_info, is_tester, get_critiques

# Create your views here.

def convert_tags(subject, message, user):
    """
    Converts the following tags in the message or subject line of an e-mail to their equivalent for the given user:
    [first] = first name
    [last] = last name
    [full] = full name
    [user] = username
    [pwrd] = password
    :param subject: string containing the subject line to be sent
    :param message: string containing the message to be sent
    :param user: User object containing data for the given user
    :return: a subject string and message string with all the tags filled in
    """
    user_info = {'[first]':user.first_name,
                 '[last]': user.last_name,
                 '[full]': user.get_full_name(),
                 '[user]': user.username,
                 '[pwrd]': get_secret(user.username.upper())}
    for tag in user_info.keys():
        subject = subject.replace(tag, user_info[tag])
        message = message.replace(tag, user_info[tag])

    return subject, message


class EmailView(View):
    template_name = 'mail/send-mail.html'

    def get(self, request):
        if request.user.is_authenticated:
            group_names = get_group_names(request.user)
        else:
            group_names = None
        if 'Administrator' in group_names or 'Supervisor' in group_names:
            supervisors = Group.objects.get(name="Supervisor").user_set.all().order_by('last_name')
            team_members = Group.objects.get(name="Team").user_set.all().order_by('last_name')
            candidates = Group.objects.get(name="Candidate").user_set.all().order_by('last_name')
            testers = Group.objects.get(name="Tester").user_set.all().order_by('last_name')
            context = {'group_names': group_names,
                       'supervisors': supervisors,
                       'team_members': team_members,
                       'candidates': candidates,
                       'testers': testers,
                       'critiques': get_critiques(request.path_info),
                       'tester': is_tester(request.user)
            }
            return render(request, self.template_name, context)
        else:
            raise PermissionDenied

    def post(self, request):
        recipients = list(set(request.POST.getlist('recipients')))
        subject_template = request.POST['subject']
        message_template = request.POST['message']
        for recipient in recipients:
            member = User.objects.get(username=recipient)
            subject, message = convert_tags(subject_template, message_template, member)
            send_mail(subject, message, 'st_basil_confirmation@confirmation.jmorris.webfactional.com',
                      [member.email], fail_silently=False,)

        return redirect('send_email')
