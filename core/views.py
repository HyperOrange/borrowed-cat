<<<<<<< Updated upstream
# core/views.py
import json, uuid, re
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
=======
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
>>>>>>> Stashed changes
from team.models import Team

TEAM_NAME_RE = re.compile(r'^[A-Za-z0-9가-힣 _-]{2,30}$')

def index_view(request):
    return render(request, "core/index.html")

@csrf_exempt  # 개발 중 임시
def create_team_ajax(request):
    if request.method != "POST":
        return HttpResponseBadRequest("invalid method")

<<<<<<< Updated upstream
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

    # Team 생성 (문자열 토큰으로)
    team = Team(team_name=team_name)
    if not getattr(team, "unique_url_token", None):
        team.unique_url_token = uuid.uuid4().hex  # 32자 문자열 토큰
    team.save()

    # ✅ reverse() 안 씀: 문자열로 직접 만듦
    redirect_url = f"/todo/{team.unique_url_token}/"

    return JsonResponse({
        "status": "success",
        "redirect_url": redirect_url,
        "team_token": team.unique_url_token,
    })
=======
    if request.method == 'POST':
        team = get_object_or_404(Team, team_id=team_id)
        deadline_date = request.POST.get('deadline_date')
        deadline_time = request.POST.get('deadline_time')

        if not deadline_date or not deadline_time:
            return render(request, 'core/set_deadline.html', {
                'error': '날짜와 시간을 모두 입력해주세요.'
            })

        team.deadline_date = deadline_date
        team.deadline_time = deadline_time
        team.save()
        return redirect('core:main_page', team_id=team_id)

    return render(request, 'core/set_deadline.html')

# 메인 페이지
def main_page(request, team_id):
    team = get_object_or_404(Team, team_id=team_id)
    todo_url = reverse('todo:list', args=[team.team_id])
    # 템플릿/JS/CSS 완전 배제: 순수 HTML 링크만 출력
    return HttpResponse(f"""
        <!doctype html>
        <meta charset="utf-8">
        <title>DEBUG Main</title>
        <h1>DEBUG MAIN for {team.team_name}</h1>
        <p><a id='go' href='{todo_url}'>▶ To-Do 로 이동</a></p>
        <p>team_id: {team.team_id}</p>
    """)

# ✅ To-Do로 서버 리다이렉트하는 전용 뷰(오버레이/JS 간섭 무시)
def go_todo(request, team_id):
    return redirect(reverse('todo:list', args=[team_id]))
>>>>>>> Stashed changes
