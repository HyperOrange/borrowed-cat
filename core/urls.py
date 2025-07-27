# MyTeamPlanner/myteam_planner/core/urls.py

from django.urls import path
from . import views # 현재 앱의 views.py 임포트

urlpatterns = [
    path('', views.index_view, name='index'), # 첫 페이지 (루트 URL)
    path('create/', views.create_team_view, name='create_team'), # 팀명 입력 페이지
    # 팀플 설정 기간 페이지 URL (team_token을 URL 파라미터로 받음)
    path('set-period/<uuid:team_token>/', views.set_period_view, name='set_period'),
]