# myteam_planner/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('todo/', include('todo_list.urls')), # todo_list 앱의 URL 패턴을 유지합니다.
    path('team/', include('team.urls')),
    # 'role_distribution' 앱을 사용하지 않으므로 해당 URL 패턴도 제거합니다.
    # path('team/<uuid:team_id>/role/', include('role_distribution.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
