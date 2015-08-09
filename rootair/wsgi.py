"""
WSGI config for balance project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

#
# Special note for mod_wsgi users
# If youe using mod_wsgi to deploy your Django application you need to include the following in your .wsgi module:

import os
# os.environ["CELERY_LOADER"] = "django"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rootair.settings")

from django.core.wsgi import get_wsgi_application
# from whitenoise.django import DjangoWhiteNoise
from dj_static import Cling

# application = get_wsgi_application()
# application = DjangoWhiteNoise(application)
application = Cling(get_wsgi_application())