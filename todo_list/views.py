# todo_list/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.utils.dateparse import parse_date

from team.models import Team, TeamMember
from .models import ToDoItem


# ----------------------------
# 공통 유틸
# ----------------------------
def _team(team_token: str) -> Team:
    """URL의 team_token으로 Team 인스턴스 가져오기"""
    return get_object_or_404(Team, unique_url_token=team_token)


def _todo_to_dict(t: ToDoItem) -> dict:
    """프론트로 내려줄 ToDoItem 직렬화"""
    return {
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "due_date": t.due_date.isoformat() if t.due_date else None,
        "priority": t.priority,
        "is_completed": t.is_completed,
        "assignee": {
            "id": t.assignee.id,
            "nickname": t.assignee.nickname,
        } if t.assignee else None,
    }


# ----------------------------
# 페이지 렌더 (템플릿 연결)
# ----------------------------
def page_list(request, team_token):
    team = _team(team_token)
    members = TeamMember.objects.filter(team=team).order_by("id")
    todos = ToDoItem.objects.filter(team=team).select_related("assignee")
    return render(
        request,
        "todo_list/page_list.html",
        {"team": team, "members": members, "todos": todos, "team_token": team_token},
    )


def page_new(request, team_token):
    team = _team(team_token)
    members = TeamMember.objects.filter(team=team).order_by("id")
    return render(
        request,
        "todo_list/page_new.html",
        {"team": team, "members": members, "team_token": team_token},
    )


def page_edit(request, team_token, todo_id):
    team = _team(team_token)
    todo = get_object_or_404(ToDoItem, team=team, id=todo_id)
    members = TeamMember.objects.filter(team=team).order_by("id")
    return render(
        request,
        "todo_list/page_edit.html",
        {"team": team, "todo": todo, "members": members, "team_token": team_token},
    )


def page_edit_date(request, team_token, todo_id):
    team = _team(team_token)
    todo = get_object_or_404(ToDoItem, team=team, id=todo_id)
    return render(
        request,
        "todo_list/page_edit_date.html",
        {"team": team, "todo": todo, "team_token": team_token},
    )


def page_edit_assignee(request, team_token, todo_id):
    team = _team(team_token)
    todo = get_object_or_404(ToDoItem, team=team, id=todo_id)
    members = TeamMember.objects.filter(team=team).order_by("id")
    return render(
        request,
        "todo_list/page_edit_assignee.html",
        {"team": team, "todo": todo, "members": members, "team_token": team_token},
    )


# ----------------------------
# AJAX 엔드포인트
# ----------------------------
@require_POST
@csrf_protect
def add_todo_item_ajax(request, team_token):
    """
    새 할 일 생성
    POST: title(필수), description, due_date(YYYY-MM-DD), priority(L/M/H), assignee_id
    """
    team = _get_team(team_token)
    title = request.POST.get("title", "").strip()
    description = request.POST.get("description", "").strip()
    due_date_str = request.POST.get("due_date", "").strip()
    priority = request.POST.get("priority", "M")
    assignee_id = request.POST.get("assignee_id")

    if not title:
        return HttpResponseBadRequest("title is required")

    due_date = parse_date(due_date_str) if due_date_str else None
    assignee = None
    if assignee_id:
        assignee = TeamMember.objects.filter(team=team, id=assignee_id).first()

    todo = ToDoItem.objects.create(
        team=team,
        title=title,
        description=description,
        due_date=due_date,
        priority=priority if priority in {"L", "M", "H"} else "M",
        assignee=assignee,
    )
    return JsonResponse({"ok": True, "todo": _todo_to_dict(todo)})


@require_POST
@csrf_protect
def toggle_todo_completed_ajax(request, team_token, todo_id):
    """완료/미완료 토글"""
    team = _get_team(team_token)
    todo = get_object_or_404(ToDoItem, team=team, id=todo_id)
    todo.is_completed = not todo.is_completed
    todo.save(update_fields=["is_completed", "updated_at"])
    return JsonResponse({"ok": True, "todo": _todo_to_dict(todo)})


@require_POST
@csrf_protect
def delete_todo_ajax(request, team_token, todo_id):
    """삭제"""
    team = _get_team(team_token)
    todo = get_object_or_404(ToDoItem, team=team, id=todo_id)
    todo.delete()
    return JsonResponse({"ok": True, "deleted_id": todo_id})


@require_POST
@csrf_protect
def update_todo_ajax(request, team_token, todo_id):
    """
    간단 수정(부분 업데이트)
    POST: title, description, due_date(YYYY-MM-DD), priority(L/M/H), assignee_id(빈문자면 해제)
    """
    team = _get_team(team_token)
    todo = get_object_or_404(ToDoItem, team=team, id=todo_id)

    title = request.POST.get("title")
    description = request.POST.get("description")
    due_date_str = request.POST.get("due_date")
    priority = request.POST.get("priority")
    assignee_id = request.POST.get("assignee_id")

    if title is not None:
        todo.title = title.strip()
    if description is not None:
        todo.description = description.strip()
    if due_date_str is not None:
        todo.due_date = parse_date(due_date_str) if due_date_str else None
    if priority in {"L", "M", "H"}:
        todo.priority = priority
    if assignee_id is not None:
        if assignee_id == "":
            todo.assignee = None
        else:
            todo.assignee = TeamMember.objects.filter(team=team, id=assignee_id).first()

    todo.save()
    return JsonResponse({"ok": True, "todo": _todo_to_dict(todo)})


def todo_deadlines_json(request, team_token):
    """달력 연동용: 마감일 있는 미완료 todos를 JSON으로 반환"""
    team = _get_team(team_token)
    todos = ToDoItem.objects.filter(team=team, due_date__isnull=False, is_completed=False).select_related("assignee")
    data = [
        {
            "id": t.id,
            "title": t.title,
            "date": t.due_date.isoformat(),  # all-day 이벤트용
            "priority": t.priority,
            "assignee": t.assignee.nickname if t.assignee else None,
            "url": "",  # 필요하면 상세 페이지 URL 연결
        }
        for t in todos
    ]
    return JsonResponse(data, safe=False)


# 내부에서만 쓰는 이름 보정 (위에서 _get_team 이름을 먼저 썼다면 아래처럼 alias)
_get_team = _team  # 가독성 위해 별칭
