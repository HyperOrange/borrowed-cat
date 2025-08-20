from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),                # 메인 홈 등 core 관리
    path('todo/', include('todo_list.urls')),      # todo
    path('team/', include('team.urls')),           # team
    path('urls/', include('url_collection.urls')), # url_collection → prefix 붙임
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
