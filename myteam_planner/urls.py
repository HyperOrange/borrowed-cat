from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('todo/', include('todo_list.urls')),
    path('team/', include('team.urls')), # team 앱의 URL을 추가합니다.
    path('role-distribution/', include('role_distribution.urls', namespace='role_distribution')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
