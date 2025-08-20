from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('<uuid:team_id>/add-member/', views.add_member, name='add_member'),
    path('<uuid:team_id>/', views.main_page, name='main_page'),  # 🔥 메인 페이지 추가
]
