# myteam_planner/myteam_planner/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # settings를 import합니다.
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# 개발 환경에서 정적 파일을 서빙하기 위한 설정입니다.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
