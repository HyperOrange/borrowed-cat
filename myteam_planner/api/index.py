# api/index.py

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myteam_planner.settings') 
# myteam_planner를 본인의 프로젝트 이름으로 변경하세요.

application = get_wsgi_application()