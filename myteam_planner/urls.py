# MyTeamPlanner/myteam_planner/myteam_planner/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # core 앱의 URL을 포함할 때 namespace를 'core'로 지정합니다.
    path('', include(('core.urls', 'core'), namespace='core')), # <-- 이 줄을 변경
    path('team/', include(('team.urls', 'team'), namespace='team')),
]