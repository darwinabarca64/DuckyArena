"""
WSGI config for quizz_project project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizz_project.settings')

application = get_wsgi_application()
