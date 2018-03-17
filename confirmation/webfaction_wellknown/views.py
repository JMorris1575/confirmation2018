from django.http import HttpResponse

# Create your views here.

def data(request, challenge_filename):
    f = open('webfaction_wellknown/.well-known/' + challenge_filename, 'r')
    data = f.read()
    f.close()
    return HttpResponse(data, content_type="text/plain")