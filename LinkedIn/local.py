from LinkedIn.base import *

ENVIRONMENT = 'local'
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'linkedin',
        'HOST': 'localhost',
        'USER':"root",
        'PASSWORD': "prashanth"
    }
}