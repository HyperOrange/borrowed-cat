from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('<uuid:team_id>/add-member/', views.add_member, name='add_member'),
]
