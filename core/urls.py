from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("create-team/", views.create_team_ajax, name="create_team"),
    path("main-page/<uuid:team_id>/", views.main_page, name="main_page"),
    path("go-todo/<uuid:team_id>/", views.go_todo, name="go_todo"),
]
