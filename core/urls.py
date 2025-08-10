from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("create-team/", views.create_team_ajax, name="create_team_ajax"),
]
