# myteam_planner/url_collection/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from team.models import Team
from .models import Link # Link 모델 불러오기 추가
import json # JSON 처리를 위해 import

def storage_view(request, team_id):
    """
    '링크 모음' 페이지를 렌더링하는 뷰입니다.
    데이터베이스에서 해당 팀의 링크 목록을 조회하여 템플릿에 전달합니다.
    """
    # team_id를 사용하여 Team 객체를 가져오고, 없으면 404 에러를 발생시킵니다.
    team = get_object_or_404(Team, pk=team_id)
    
    # 데이터베이스에서 해당 팀의 모든 링크를 가져옵니다.
    links = Link.objects.filter(team=team)
    
    context = {
        'team': team,
        'links': links,
    }
    
    return render(request, 'url_collection/storage.html', context)

def add_url_view(request, team_id):
    """
    링크 추가 페이지를 렌더링하고 POST 요청을 처리합니다.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            link_url = data.get('link_url')
            link_title = data.get('link_title')
            
            # team_id를 사용하여 Team 객체를 가져옵니다.
            team = get_object_or_404(Team, pk=team_id)
            
            # Link 모델을 사용하여 데이터베이스에 링크를 저장합니다.
            Link.objects.create(team=team, url=link_url, title=link_title)
            
            return JsonResponse({'success': True, 'message': '링크가 성공적으로 추가되었습니다.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '잘못된 JSON 형식입니다.'}, status=400)
    else:
        # GET 요청일 경우 HTML 페이지를 렌더링합니다.
        team = get_object_or_404(Team, pk=team_id)
        return render(request, 'url_collection/add_url.html', {'team': team})

def test_page(request):
    """
    테스트 페이지를 렌더링하는 뷰입니다.
    """
    return render(request, "url_collection/test.html")