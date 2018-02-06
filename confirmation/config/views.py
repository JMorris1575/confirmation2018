from django.shortcuts import render, redirect
from django.views import View


class HelpView(View):
    template_name = 'help.html'

    def get(self, request, page_name):
        context = {'page_file_name':page_name + '.html'}
        return render(request, self.template_name, context)
