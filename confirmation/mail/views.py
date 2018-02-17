from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail

from config.mixins import PageMixin
from config.settings.base import get_secret

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

    def post(self, request):
        recipients = request.POST.getlist('recipients')
        subject_template = request.POST['subject']
        message_template = request.POST['message']
        for recipient in recipients:
            member = User.objects.get(username=recipient)
            subject, message = convert_tags(subject_template, message_template, member)
            send_mail(subject, message, 'FrJamesMorris@gmail.com', [member.email], fail_silently=False,)

        return redirect('send_email')
