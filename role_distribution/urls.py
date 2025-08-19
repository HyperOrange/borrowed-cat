# role_distribution/urls.py
from django.urls import path
from . import views

app_name = 'role_distribution'

urlpatterns = [
    path('<uuid:team_id>/', views.role_distribution_page, name='role_distribution_page'),
    path('<uuid:team_id>/update-roles/', views.update_role_assignments, name='update_role_assignments'),
    path('<uuid:team_id>/add-role/', views.add_new_role, name='add_new_role'),
    path('<uuid:team_id>/ai-assign/', views.handle_ai_assign, name='handle_ai_assign'),
]