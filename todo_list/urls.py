from django.urls import path
from . import views

app_name = "todo_list"

urlpatterns = [
    # To-Do 메인 리스트
    path("<str:team_token>/", views.page_list, name="list"),

    # CRUD
    path("<str:team_token>/new/", views.create_item, name="new"),
    path("<str:team_token>/<int:pk>/edit/", views.update_item, name="edit"),
    path("<str:team_token>/<int:pk>/toggle/", views.toggle_done, name="toggle"),
    path("<str:team_token>/<int:pk>/delete/", views.delete_item, name="delete"),
]
