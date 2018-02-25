from django.shortcuts import render, redirect
from django.views import View

from .models import Critique

# Create your views here.

class CritiqueView(View):

    def post(self, request):
        page_url = request.POST['page_url']
        critique = request.POST['critique']
        critique = Critique(path=page_url, user=request.user, text=critique)
        critique.save()
        return redirect(page_url)


class ToggleCritiquesView(View):

    def get(self, request):
        if request.session.get('critiques_visible', True):
            request.session['critiques_visible'] = False
        else:
            request.session['critiques_visible'] = True
        return redirect('/activity/welcome/')