"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named `application`.
"""

import os
from django.core.asgi import get_asgi_application

# Set default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# ASGI application
application = get_asgi_application()