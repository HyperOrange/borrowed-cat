# myteam_planner/url_collection/urls.py

from django.urls import path
from . import views

# 이 앱의 이름을 'url_collection'으로 지정하여
# {% url 'url_collection:storage' %}와 같이 사용할 수 있게 합니다.
app_name = 'url_collection'

urlpatterns = [
    # team_id를 UUID 형식으로 받아 뷰에 전달합니다.
    # 이름은 main_page.html의 {% url %} 태그와 일치하도록 'storage'로 설정합니다.
    path("<uuid:team_id>/storage/", views.storage_view, name="storage"),
    # 링크 추가 페이지로 이동하는 새로운 URL 패턴을 추가합니다.
    path("<uuid:team_id>/add_url/", views.add_url_view, name="add_url"),
    # 테스트 페이지 URL입니다.
    path("test/", views.test_page, name="test_page"),
]