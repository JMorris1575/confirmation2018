from django.shortcuts import render
from django.views import View
from config.mixins import PageMixin

# Create your views here.


class EmailView(View):
    template_name = 'mail/send-mail.html'

    def get(self, request):
        if request.user.is_authenticated:
            group_names = PageMixin.get_group_names(self, request.user)
        else:
            group_names = None
        return render(request, self.template_name, context={'group_names':group_names})
