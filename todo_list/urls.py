from django.urls import path
from . import views

app_name = 'todo_list'

urlpatterns = [
    # 할 일 목록 페이지
    path('<uuid:team_id>/', views.todo_list_page, name='list'),
    # 할 일 추가 페이지
    path('<uuid:team_id>/add/', views.todo_add_page, name='add'),
]
