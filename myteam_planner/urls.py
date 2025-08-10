
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('role-distribution/', include('role_distribution.urls')), # 'role_distribution'을 'role-distribution'으로 수정
    # 다른 앱의 URL도 여기에 추가하세요 (예: path('team/', include('team.urls')),)
]

# 개발 환경에서만 정적 파일을 서빙하도록 설정합니다.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])