from django.shortcuts import render, redirect
from django.views import View

from .models import Critique
from config.utilities import get_group_names, get_response_info, is_tester, get_critiques

# Create your views here.

class CritiqueView(View):

    def post(self, request):
        page_url = request.POST['page_url']
        critique = request.POST['critique'].strip()
        if critique:
            critique = Critique(path=page_url, user=request.user, text=critique)
            critique.save()
        return redirect(page_url)


class EditCritiqueView(View):
    template_name = 'consultants/edit-critique.html'

    def get(self, request, pk=None):
        page_url = request.META['QUERY_STRING'].replace('next=', '')        # the page from which this came
        critique = Critique.objects.get(pk=pk)
        context = {'page_url': page_url,
                   'critique': critique,
                   'critiques': get_critiques(request.path_info),
                   'tester': is_tester(request.user)}
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        page_url = request.POST['page_url']     # page_url obtained from get method passed through edit-critique.html
        if request.POST['button'] == 'OK':
            critique = Critique.objects.get(pk=pk)
            critique.text = request.POST['entry']
            critique.save()
        return redirect(page_url)


class DeleteCritiqueView(View):
    template_name = 'consultants/delete_critique.html'

    def get(self, request, pk=None):
        page_url = request.META['QUERY_STRING'].replace('next=', '')        # handed through edit-critique.html
        critique = Critique.objects.get(pk=pk)
        context = {'page_url': page_url,
                   'critique': critique,}
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        page_url = request.POST['page_url']         # page_url as obtained from get method above
        if request.POST['user-choice'] == 'Delete':
            critique = Critique.objects.get(pk=pk)
            critique.delete()

        return redirect(page_url)



class ToggleCritiquesView(View):

    def get(self, request):
        if request.session.get('critiques_visible', False):
            request.session['critiques_visible'] = False
        else:
            request.session['critiques_visible'] = True
        return redirect(request.META['QUERY_STRING'].replace('next=', ''))