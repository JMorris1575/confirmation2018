from django.http import HttpResponse

import os, sys, logging
import config.settings.base as base

# Create your views here.

def data(request, challenge_filename):
    # logging.basicConfig(filename=os.path.join(base.BASE_DIR, 'info.log'), format='%(asctime)s %(message)s',
    #                     datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    # logging.info('*** got to views.py data with challenge_filename = %s', challenge_filename)
    # logging.info('BASE_DIR = %s', base.BASE_DIR)
    # logger = logging.getLogger(__name__)
    # logger.info('*** got to views.py data with challenge_filename = %s', challenge_filename)
    # logger.info('BASE_DIR = %s', base.BASE_DIR)
    # print("Hello World!", file = base.BASE_DIR + '/printTest.txt')
    path_to_file = './webapps/conf18/confirmation/webfaction_wellknown/.well-known/acme-challenge/'
    path_to_file = os.path.join(base.BASE_DIR, '.well-known', 'acme-challenge')
    f = open(os.path.join(path_to_file, challenge_filename), 'r')
    data = f.read()
    f.close()
    #return HttpResponse(data, content_type="text/plain")
    return HttpResponse(path_to_file, content_type="text/plain")