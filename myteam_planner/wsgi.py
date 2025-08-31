"""
WSGI config for myteam_planner project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

# myteam_planner/wsgi.py

import os
import sys
from django.core.wsgi import get_wsgi_application

# 프로젝트 경로를 Python path에 추가
sys.path.append('/var/task')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myteam_planner.settings')

application = get_wsgi_application()

# Vercel을 위한 핸들러
def handler(request, context):
    return application(request, context)