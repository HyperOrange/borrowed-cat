# role_distribution/urls.py
from django.urls import path
from . import views

app_name = 'role_distribution'

urlpatterns = [
    path('<uuid:team_id>/', views.role_distribution_page, name='role_page'),
    path('<uuid:team_id>/random-assign/', views.random_assign_roles, name='random_assign'),
]