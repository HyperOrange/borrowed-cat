# myteam_planner/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('core.urls', 'core'), namespace='core')),
    path('team/', include(('team.urls', 'team'), namespace='team')),
    # 역할 분배 앱의 URL을 기존 방식에 맞춰 추가합니다.
    path('role/', include(('role_distribution.urls', 'role_distribution'), namespace='role_distribution')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)