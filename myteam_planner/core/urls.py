from django.urls import path
from . import views

urlpatterns = [
    # 최상위 경로('/')에 views.py의 index 함수를 연결합니다.
    path('', views.index, name='index'),
    # 'create-team/' 경로에 views.py의 create_team 함수를 연결합니다.
    path('create-team/', views.create_team, name='create_team'),
    # 'set-deadline/' 경로에 views.py의 set_deadline 함수를 연결합니다.
    path('set-deadline/', views.set_deadline, name='set_deadline'),
]
