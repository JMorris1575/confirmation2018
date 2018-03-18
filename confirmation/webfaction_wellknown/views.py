from django.http import HttpResponse

import os

# Create your views here.

def data(request, challenge_filename):
    path_to_file = './webapps/conf18/confirmation/webfaction_wellknown/.well-known/acme-challenge/'
    f = open(path_to_file + challenge_filename, 'r')
    data = f.read()
    f.close()
    return HttpResponse(data, content_type="text/plain")