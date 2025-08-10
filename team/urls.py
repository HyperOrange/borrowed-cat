# MyTeamPlanner/myteam_planner/team/urls.py

from django.urls import path
from . import views # 현재 앱의 views.py 임포트

urlpatterns = [
    # team_token을 받아 메인 페이지를 보여주는 URL
    path('<str:team_token>/', views.main_page_view, name='main_page'),
]