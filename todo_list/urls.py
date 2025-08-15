from django.urls import path
from . import views

app_name = 'todo_list'

urlpatterns = [
    path('<uuid:team_id>/', views.list, name='list'),
    path('<uuid:team_id>/new/', views.new, name='new'),
]
