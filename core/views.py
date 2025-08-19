# core/views.py
import json, uuid, re
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from team.models import Team

# 팀 이름 검증 (한글/영문/숫자/공백/-/_ 만 허용, 2~30자)
TEAM_NAME_RE = re.compile(r'^[A-Za-z0-9가-힣 _-]{2,30}$')

# 첫 페이지
def index_view(request):
    return render(request, "core/index.html")

# AJAX 팀 생성 (프론트에서 fetch 사용 시)
@csrf_exempt  # 개발 중 CSRF 임시 무시
def create_team_ajax(request):
    if request.method != "POST":
        return HttpResponseBadRequest("invalid method")

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("invalid json")

    team_name = (data.get("team_name") or "").strip()
    if not TEAM_NAME_RE.match(team_name):
        return JsonResponse(
            {"status": "error", "message": "팀명은 2~30자, 한글/영문/숫자/공백/-/_만 가능합니다."},
            status=400,
        )

    # Team 생성
    team = Team(team_name=team_name)
    if not getattr(team, "unique_url_token", None):
        team.unique_url_token = uuid.uuid4().hex  # 32자리 문자열 토큰
    team.save()

    # 바로 To-Do 페이지로 연결될 URL
    redirect_url = f"/todo/{team.unique_url_token}/"

    return JsonResponse({
        "status": "success",
        "redirect_url": redirect_url,
        "team_token": team.unique_url_token,
    })

# 메인 페이지 (DEBUG 모드 - 순수 HTML로 확인 가능)
def main_page(request, team_id):
    team = get_object_or_404(Team, team_id=team_id)
    try:
        todo_url = reverse("todo:list", args=[team.team_id])
    except Exception as e:
        print(f"[WARN] todo:list URL 생성 실패: {e}")
        todo_url = "#"

    return HttpResponse(f"""
        <!doctype html>
        <meta charset="utf-8">
        <title>DEBUG Main</title>
        <h1>DEBUG MAIN for {team.team_name}</h1>
        <p><a id='go' href='{todo_url}'>▶ To-Do 로 이동</a></p>
        <p>team_id: {team.team_id}</p>
    """)

# To-Do 바로 리다이렉트용
def go_todo(request, team_id):
    return redirect(reverse("todo:list", args=[team_id]))
