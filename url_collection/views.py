# url_collection/views.py
from django.shortcuts import render, get_object_or_404
from team.models import Team   # ✅ Team 모델 불러오기 (팀 정보 확인용)

# 링크 모음 페이지
def url_collection(request, team_id):
    team = get_object_or_404(Team, pk=team_id)   # ✅ team_id 기준으로 팀 조회
    return render(request, 'url_collection/url_collection.html', {'team': team})

def test_page(request):
    return render(request, "url_collection/test.html")
