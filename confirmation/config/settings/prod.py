"""
This file will need some work before the website is hosted by WebFaction.
See the christmas17 project.
"""

from .base import *

import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('PROD_DATABASE_NAME'),
        'USER': get_secret('PROD_DATABASE_USER'),
        'PASSWORD': get_secret('PROD_DATABASE_PASSWORD'),
        'HOST': get_secret('PROD_DATABASE_HOST'),
        'PORT': get_secret('PROD_DATABASE_PORT')
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.01/howto/static-files/

# STATIC_ROOT = fill in with webfactional information
#STATIC_URL = fill in with webfactional information
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static', 'site'), )

EMAIL_HOST = get_secret('EMAIL_HOST')
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = get_secret('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = get_secret('SERVER_EMAIL')

