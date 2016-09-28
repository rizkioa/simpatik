"""
WSGI config for simpdu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simpdu.settings")

from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

application = Sentry(get_wsgi_application())
