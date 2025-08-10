from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-team/', views.create_team, name='create_team'),
    path('set-deadline/', views.set_deadline, name='set_deadline'),
    path('main-page/<uuid:team_id>/', views.main_page, name='main_page'), # 메인 페이지 URL 추가
]
