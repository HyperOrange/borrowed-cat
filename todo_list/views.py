# todo_list/views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import ToDoItem
from .forms import ToDoItemForm
from team.models import Team, TeamMember


# ----------------------------
# 공통 유틸
# ----------------------------
def _get_team(team_token):
    """Team 모델의 unique_url_token으로 가져오기"""
    return get_object_or_404(Team, unique_url_token=team_token)


# ----------------------------
# 페이지 렌더링
# ----------------------------
def page_list(request, team_token):
    """To-Do 리스트 페이지"""
    team = _get_team(team_token)
    items = (
        ToDoItem.objects
        .filter(team=team)
        .select_related("assignee")
        .order_by("is_done", "due_at", "-id")
    )

    # 담당자 필터 (선택)
    assignee_id = request.GET.get("assignee")
    if assignee_id:
        items = items.filter(assignee_id=assignee_id)

    # 신규 추가 폼 (모달용)
    form = ToDoItemForm()
    form.fields["assignee"].queryset = TeamMember.objects.filter(team=team)

    context = {
        "team": team,
        "items": items,
        "form": form,
        "assignees": TeamMember.objects.filter(team=team),
    }
    return render(request, "todo_list/list.html", context)


# ----------------------------
# CRUD 동작
# ----------------------------
@require_POST
def create_item(request, team_token):
    team = _get_team(team_token)
    form = ToDoItemForm(request.POST)
    form.fields["assignee"].queryset = TeamMember.objects.filter(team=team)
    if form.is_valid():
        item = form.save(commit=False)
        item.team = team
        item.created_by = None  # 로그인 연동 시 작성자 매핑 가능
        item.save()
        messages.success(request, "할 일이 추가되었습니다.")
    else:
        messages.error(request, "입력 값을 확인해주세요.")
    return redirect(reverse("todo:list", args=[team.unique_url_token]))


def update_item(request, team_token, pk):
    team = _get_team(team_token)
    item = get_object_or_404(ToDoItem, pk=pk, team=team)

    if request.method == "POST":
        form = ToDoItemForm(request.POST, instance=item)
        form.fields["assignee"].queryset = TeamMember.objects.filter(team=team)
        if form.is_valid():
            form.save()
            messages.success(request, "할 일이 수정되었습니다.")
            return redirect(reverse("todo:list", args=[team.unique_url_token]))
    else:
        form = ToDoItemForm(instance=item)
        form.fields["assignee"].queryset = TeamMember.objects.filter(team=team)

    return render(request, "todo_list/edit.html", {"team": team, "form": form, "item": item})


@require_POST
def toggle_done(request, team_token, pk):
    team = _get_team(team_token)
    item = get_object_or_404(ToDoItem, pk=pk, team=team)
    item.is_done = not item.is_done
    item.save(update_fields=["is_done", "updated_at"])
    return redirect(reverse("todo:list", args=[team.unique_url_token]))


@require_POST
def delete_item(request, team_token, pk):
    team = _get_team(team_token)
    item = get_object_or_404(ToDoItem, pk=pk, team=team)
    item.delete()
    messages.success(request, "삭제되었습니다.")
    return redirect(reverse("todo:list", args=[team.unique_url_token]))
