from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
<<<<<<< Updated upstream
    path("", views.index_view, name="index"),
    path("create-team/", views.create_team_ajax, name="create_team_ajax"),
=======
    path('', views.index, name='index'),
    path('create-team/', views.create_team, name='create_team'),
    path('set-deadline/', views.set_deadline, name='set_deadline'),
    path('main-page/<uuid:team_id>/', views.main_page, name='main_page'),

    # ✅ To-Do로 리다이렉트
    path('go-todo/<uuid:team_id>/', views.go_todo, name='go_todo'),
>>>>>>> Stashed changes
]
