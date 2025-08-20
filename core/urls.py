# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('create-team/', views.create_team, name='create_team'),
    path('set-deadline/', views.set_deadline, name='set_deadline'),
    path('main-page/<uuid:team_id>/', views.main_page, name='main_page'),
    path("url-collection/", views.url_collection, name="url_collection"),
]