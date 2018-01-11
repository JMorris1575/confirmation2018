from django.shortcuts import render
from django.views import View

# Create your views here.

class WelcomeView(View):
    template_name = 'activity/welcome.html'

    def get(self, request):
        print("request['POST'] = ", request['POST'])
        return render(request, self.template_name)

    def post(self, request):
        print("request['POST'] = ", request['POST'])
        return render(request, self.template_name)