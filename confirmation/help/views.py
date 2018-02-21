from django.shortcuts import render, redirect
from django.views import View
from .models import HelpCategory, HelpPage
from config.mixins import PageMixin


class HelpView(View):
    template_name = 'help/help.html'

    def get(self, request, category_name, page_number=None):
        category = HelpCategory.objects.get(name=category_name)
        if request.user.is_authenticated:
            group_names = PageMixin.get_group_names(request.user)
        else:
            group_names = None
        if not page_number:
            context = {'page_file_name': 'help/' + category_name + '.html',
                       'category': category_name, 'previous': None, 'next': None,
                       'group_names': group_names}
        else:
            help_page = HelpPage.objects.get(category=category, number=page_number)
            page_count = len(HelpPage.objects.filter(category=category))
            page_number = help_page.number
            previous_page_num = page_number - 1
            if previous_page_num <= 0:
                previous = None
            else:
                previous = previous_page_num
            next_page_num = page_number + 1
            if next_page_num > page_count:
                next_page = None
            else:
                next_page = next_page_num
            context = {'page_file_name': 'help/' + help_page.name + '.html',
                       'category': category_name, 'previous': previous, 'next': next_page,
                       'group_names': group_names}
        return render(request, self.template_name, context)
