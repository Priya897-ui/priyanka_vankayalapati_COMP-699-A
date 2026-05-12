"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named `application`.
This is used by Django's development server and production servers like Gunicorn.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# WSGI application
application = get_wsgi_application()