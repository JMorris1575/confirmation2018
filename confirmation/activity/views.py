from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import Group
from .models import Activity, Page, Response, Choice
from config.utilities import get_group_names, get_response_info, is_tester, get_critiques,\
                            get_welcome_report, get_summary_report

import datetime

# Create your views here.

class WelcomeView(View):
    template_name = 'activity/welcome.html'

    def get(self, request):
        activities = Activity.objects.filter(publish_date__lte=datetime.date.today(),
                                             closing_date__gt=datetime.date.today(),
                                             visible=True)
        data = []
        for activity in activities:
            pages = Page.objects.filter(activity=activity)
            page_count = len(pages)
            completed = len(Response.objects.filter(user=request.user, activity=activity, completed=True))
            if page_count != 0:
                percent_completed = completed/page_count * 100
                if percent_completed < 100:
                    msg = '{:.1f}'.format(percent_completed) + '% Complete'
                else:
                    msg = 'Finished!'
            else:
                msg = 'Not Yet Available'
            data.append((activity, msg))
        group_names = get_group_names(request.user)
        # set 'critiques_visible' to true if it is not set
        try:
            test = request.session['critiques_visible']
        except KeyError:
            request.session['critiques_visible'] = True
        return render(request, self.template_name,
                      {'data': data,
                       'group_names': group_names,
                       'critiques': get_critiques(request.path_info),
                       'tester': is_tester(request.user),
                       'reports': get_welcome_report()})


class SummaryView(View):
    template_name = 'activity/summary.html'

    def get(self, request, activity_slug):
        activity = Activity.objects.get(slug=activity_slug)
        pages = Page.objects.filter(activity=activity.pk)
        responses = Response.objects.filter(user=request.user, activity=activity.pk)
        data = []
        first_pass = True                          # this changes as soon as an incomplete page is found
        for page in pages:
            if responses.filter(page=page.pk) and first_pass:
                data.append((page, 'Completed'))    # If user has a response, call the page complete
            elif first_pass:
                data.append((page, 'Up next...'))   # This is the next page to do
                first_pass = False                  # after that, enter 'Pending' for the rest of the pages
            else:
                data.append((page, 'Pending'))
        group_names = get_group_names(request.user)
        return render(request, self.template_name, {'activity': activity,
                                                    'data': data,
                                                    'group_names': group_names,
                                                    'critiques': get_critiques(request.path_info),
                                                    'tester': is_tester(request.user),
                                                    'reports': get_summary_report(activity)})


class PageView(View):

    def get(self, request, activity_slug, page_index):
        activity, page, responses, context = get_response_info(request.user, activity_slug, page_index)
        if not page.allowed(request.user, activity_slug, page_index):
            return redirect('summary', activity_slug)
        if page.page_type == 'IN':
            self.template_name = 'activity/instruction.html'
        elif page.page_type == 'ES':
            self.template_name = 'activity/essay.html'
        elif page.page_type == 'MC':
            self.template_name = 'activity/multi-choice.html'
            choices = Choice.objects.filter(page=page)
            context['choices'] = choices
        elif page.page_type == 'TF':
            self.template_name = 'activity/true-false.html'
        elif page.page_type == 'DS':
            return redirect('discussion', activity_slug, page_index)
        context['critiques'] = get_critiques(request.path_info)
        context['tester'] = is_tester(request.user)
        return render(request, self.template_name, context)

    def post(self, request, activity_slug=None, page_index=None):
        activity = Activity.objects.get(slug=activity_slug)
        page = Page.objects.get(activity=activity.pk, index=page_index)
        if page.page_type == 'IN':
            response = Response(user=request.user, activity=activity, page=page, completed=True)
            response.save()
        elif page.page_type == 'ES':
            response = Response(user=request.user, activity=activity, page=page,
                                essay=request.POST['essay'].strip(), completed=True)
            response.save()
        elif page.page_type == 'MC':
            choices = Choice.objects.filter(page=page)
            try:
                choice_index = request.POST['choice']
            except (KeyError, Choice.DoesNotExist):
                self.template_name = 'activity/multi-choice.html'
                context = {'activity':activity, 'page':page, 'choices':choices, 'response':None}
                context['error_message'] = 'You must choose one of the responses below.'
                return render(request, self.template_name, context)
            choice = choices.get(index=choice_index)
            response = Response(user=request.user, activity=activity,
                                page=page, multi_choice=str(choice_index),
                                completed=True)
            if not page.opinion:
                response.correct = choice.correct
            response.save()
        elif page.page_type == 'TF':
            try:
                user_response_string = request.POST['choice']
            except KeyError:
                self.template_name = 'activity/true-false.html'
                context = {'activity':activity, 'page':page, 'response':None}
                context['error_message'] = 'You must select either True or False.'
                return render(request, self.template_name, context)
            user_response = (user_response_string == 'True')
            response = Response(user=request.user, activity=activity,
                                page=page, true_false=user_response,
                                completed=True)
            if not page.opinion:
                response.correct = (user_response == page.tf_answer)
            response.save()
        elif page.page_type == 'DS':
            return redirect('discussion', activity_slug, page_index)

        return redirect('page', activity_slug, page_index )


class PageEditView(View):

    def get(self, request, activity_slug=None, page_index=None):
        activity, page, responses, context = get_response_info(request.user, activity_slug, page_index)
        if page.page_type == 'ES':
            self.template_name = 'activity/essay_edit.html'
        elif page.page_type == 'MC':
            self.template_name = 'activity/multi-choice-edit.html'
            choices = Choice.objects.filter(page=page)
            context['choices'] = choices
        elif page.page_type == 'TF':
            response = context['response']
            response.true_false = not response.true_false
            response.save()
            return redirect('page', activity_slug, page_index)
        context['critiques'] = get_critiques(request.path_info),
        context['tester'] = is_tester(request.user)
        return render(request, self.template_name, context)

    def post(self, request, activity_slug=None, page_index=None):
        activity, page, responses, context = get_response_info(request.user, activity_slug, page_index)
        response = context['response']
        if request.POST['button'] == 'OK':            # if it's 'Cancel' skip right to the redirect
            if page.page_type == 'ES':                # note: the editing for TF pages takes place in the get method
                response.essay = request.POST['essay'].strip()
                response.save()
            elif page.page_type == 'MC':
                response.multi_choice = request.POST['choice']
                response.save()

        return redirect('page', activity_slug, page_index)


class PageDeleteView(View):

    def get(self, request, activity_slug=None, page_index=None):
        activity, page, responses, context = get_response_info(request.user, activity_slug, page_index)
        if page.page_type == 'ES':
            self.template_name = 'activity/essay_delete.html'
        if page.page_type == 'MC':
            self.template_name = 'activity/multi-choice-delete.html'
        if page.page_type == 'TF':
            self.template_name = 'activity/true-false-delete.html'
        return render(request, self.template_name, context)

    def post(self, request, activity_slug=None, page_index=None):
        activity, page, responses, context = get_response_info(request.user, activity_slug, page_index)
        if request.POST['button'] == 'Delete':
            response = responses[0]
            response.delete()
            return redirect('summary', activity_slug)
        else:
            return redirect('page', activity_slug, page_index)


class ReportView(View):

    template_name = 'activity/reports.html'

    def get(self, request):
        return render(request, self.template_name, {'group_names': get_group_names(request.user),
                                                    'critiques': get_critiques(request.path_info),
                                                    'tester': is_tester(request.user)})