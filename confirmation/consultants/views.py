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
        critique = Critique.objects.get(pk=pk)
        context = {'critique': critique,
                   'critiques': get_critiques(request.path_info),
                   'tester': is_tester(request.user)}
        return render(request, self.template_name, context)


class ToggleCritiquesView(View):

    def get(self, request):
        if request.session.get('critiques_visible', False):
            request.session['critiques_visible'] = False
        else:
            request.session['critiques_visible'] = True
        return redirect(request.META['QUERY_STRING'].replace('next=', ''))