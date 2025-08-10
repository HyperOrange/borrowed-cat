# core/views.py
import json, uuid, re
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from team.models import Team

TEAM_NAME_RE = re.compile(r'^[A-Za-z0-9가-힣 _-]{2,30}$')

def index_view(request):
    return render(request, "core/index.html")

@csrf_exempt  # 개발 중 임시
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
