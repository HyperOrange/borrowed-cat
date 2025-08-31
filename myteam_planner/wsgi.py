"""
WSGI config for myteam_planner project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

# myteam_planner/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myteam_planner.settings')

application = get_wsgi_application()
app = application  # Vercel에서 인식하기 위해 추가