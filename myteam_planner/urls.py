# myteam_planner/myteam_planner/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('core.urls', 'core'), namespace='core')),
    path('team/', include(('team.urls', 'team'), namespace='team')),
    path('todo/', include(('todo_list.urls', 'todo'), namespace='todo')),  # ✅ 한 줄이면 충분
]
