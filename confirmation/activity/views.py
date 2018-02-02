from django.shortcuts import render, redirect
from django.views import View
from .models import Activity, Page, Response, Choice
from config.mixins import ResponseMixin

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
        return render(request, self.template_name, {'data': data})

    def post(self, request):
        return render(request, self.template_name)


class SummaryView(View):
    template_name = 'activity/summary.html'

    def get(self, request, activity_slug):
        activity = Activity.objects.get(slug=activity_slug)
        pages = Page.objects.filter(activity=activity.pk)
        responses = Response.objects.filter(user=request.user, activity=activity.pk)
        data = []
        changing_msg = 'Up next...'
        for page in pages:
            if responses.filter(page=page.pk):
                data.append((page, 'Completed'))    # If user has a response, call the page complete
            else:
                data.append((page, changing_msg))   # The first time we get here changing_msg='Up next...'
                changing_msg = 'Pending'            # after that, changing_msg='Pending' for the rest of the pages
        return render(request, self.template_name, {'activity': activity,
                                                    'data': data})


# class ResponseMixin:
#
#     """
#     This mixin gets single responses from the Response model depending on the user, activity and page
#     """
#
#     def get_response_info(self, user=None, activity_slug=None, page_index=None):
#         activity = Activity.objects.get(slug=activity_slug)
#         page = Page.objects.get(activity=activity, index=page_index)
#         try:
#             response = Response.objects.get(user=user, activity=activity, page=page)
#         except Response.DoesNotExist:
#             response = None
#         return activity, page, response


class PageView(ResponseMixin, View):

    def get(self, request, activity_slug, page_index):
        activity, page, responses, context = self.get_response_info(request.user, activity_slug, page_index)
        if not page.allowed(request.user, activity_slug, page_index):
            return redirect('summary', activity_slug)
        if page.page_type == 'IN':
            self.template_name = 'activity/instructions.html'
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
                user_response = request.POST['choice']
            except KeyError:
                self.template_name = 'activity/true-false.html'
                context = {'activity':activity, 'page':page, 'response':None}
                context['error_message'] = 'You must select either True or False.'
                return render(request, self.template_name, context)
            response = Response(user=request.user, activity=activity,
                                page=page, true_false=user_response,
                                completed=True)
            if not page.opinion:
                response.correct = page.tf_answer
            response.save()
        elif page.page_type == 'DS':
            return redirect('discussion', activity_slug, page_index)

        return redirect('page', activity_slug, page_index )


class PageEditView(ResponseMixin, View):

    def get(self, request, activity_slug=None, page_index=None):
        activity, page, responses, context = self.get_response_info(request.user, activity_slug, page_index)
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

        return render(request, self.template_name, context)

    def post(self, request, activity_slug=None, page_index=None):
        activity, page, response = self.get_response_info(request.user, activity_slug, page_index)
        if page.page_type == 'ES':
            response.essay = request.POST['essay'].strip()
            response.save()
        elif page.page_type == 'MC':
            response.multi_coice = request.POST['choice']
            response.save()

        return redirect('page', activity_slug, page_index)


class PageDeleteView(ResponseMixin, View):

    def get(self, request, activity_slug=None, page_index=None):
        activity, page, responses, context = self.get_response_info(request.user, activity_slug, page_index)
        if page.page_type == 'ES':
            self.template_name = 'activity/essay_delete.html'
        if page.page_type == 'MC':
            self.template_name = 'activity/multi-choice-delete.html'
        if page.page_type == 'TF':
            self.template_name = 'activity/true-false-delete.html'
        return render(request, self.template_name, context)

    def post(self, request, activity_slug=None, page_index=None):
        activity, page, responses, context = self.get_response_info(request.user, activity_slug, page_index)
        if request.POST['user-choice'] == 'Delete':
            response = responses[0]
            response.delete()
            return redirect('summary', activity_slug)
        else:
            return redirect('page', activity_slug, page_index)
