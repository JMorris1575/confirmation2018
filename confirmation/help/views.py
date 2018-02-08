from django.shortcuts import render, redirect
from django.views import View
from .models import HelpPage


class HelpView(View):
    template_name = 'help/help.html'

    def get(self, request, page_name, page_number=None):
        print('help.views.py: page_number = ', page_number)
        if not page_number:
            context = {'page_file_name': 'help/' + page_name + '.html'}
        else:
            help_page = HelpPage.objects.get(page=page_number)
            context = {'page_file_name': 'help/' + help_page.page_name + '.html'}
        return render(request, self.template_name, context)
