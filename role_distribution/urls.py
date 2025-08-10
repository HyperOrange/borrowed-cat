from django.urls import path
from . import views

urlpatterns = [
    # 이 부분은 URL 경로가 비어있으므로, 메인 프로젝트 urls.py의 경로를 따라갑니다.
    path('', views.role_distribution_view, name='role-distribution'), 
]