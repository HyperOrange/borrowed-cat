from django.urls import path
from . import views

app_name = 'url_collection'

urlpatterns = [
    path("<uuid:team_id>/", views.url_collection, name="url_collection_page"),
    path("test/", views.test_page, name="test_page"),
]
