# todo_list/urls.py
from django.urls import path
from . import views

<<<<<<< Updated upstream
app_name = "todo"  # ✅ namespace와 동일하게

urlpatterns = [
    # 페이지 5개
    path("<str:team_token>/", views.page_list, name="list"),                         # 투두리스트_1 (메인)
    path("<str:team_token>/new/", views.page_new, name="new"),                      # 신규 추가
    path("<str:team_token>/edit/<int:todo_id>/", views.page_edit, name="edit"),     # 수정(메인)
    path("<str:team_token>/edit/<int:todo_id>/date/", views.page_edit_date, name="edit_date"),  # 수정(날짜)
    path("<str:team_token>/edit/<int:todo_id>/assignee/", views.page_edit_assignee, name="edit_assignee"),  # 수정(담당자)

    # AJAX (이미 만들었던 엔드포인트)
    path("<str:team_token>/add/", views.add_todo_item_ajax, name="add"),
    path("<str:team_token>/toggle/<int:todo_id>/", views.toggle_todo_completed_ajax, name="toggle"),
    path("<str:team_token>/delete/<int:todo_id>/", views.delete_todo_ajax, name="delete"),
    path("<str:team_token>/update/<int:todo_id>/", views.update_todo_ajax, name="update"),
    path("<str:team_token>/deadlines.json", views.todo_deadlines_json, name="deadlines_json"),
=======
app_name = "todo"
urlpatterns = [
    path("<uuid:team_id>/", views.page_list, name="list"),
    path("<uuid:team_id>/new/", views.create_item, name="new"),
    path("<uuid:team_id>/<int:pk>/edit/", views.update_item, name="edit"),
    path("<uuid:team_id>/<int:pk>/toggle/", views.toggle_done, name="toggle"),
    path("<uuid:team_id>/<int:pk>/delete/", views.delete_item, name="delete"),
>>>>>>> Stashed changes
]

