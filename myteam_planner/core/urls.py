# MyTeamPlanner/myteam_planner/core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    # 이 부분이 중요합니다! 'name'이 'create_team_ajax'로 정확히 정의되었는지 확인하세요.
    path('create-ajax/', views.create_team_ajax_view, name='create_team_ajax'),
    path('set-period/<uuid:team_token>/', views.set_period_view, name='set_period'),
]