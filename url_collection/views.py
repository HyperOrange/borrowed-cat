from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from .models import URLStorage

def add_url_view(request, team_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')
            
            print(f"받은 URL: {url}")  # 디버그용
            
            if not url:
                return JsonResponse({'success': False, 'error': 'URL이 필요합니다.'})
            
            # URL이 http:// 또는 https://로 시작하지 않으면 추가
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # URLStorage 모델을 사용해서 저장
            url_storage = URLStorage.objects.create(
                team_id=str(team_id),  # UUID를 문자열로 변환
                url=url,
                title=url  # 일단 URL을 title로 사용
            )
            
            print(f"URL 저장됨: {url_storage.id}")  # 디버그용
            
            return JsonResponse({'success': True})
        except Exception as e:
            print(f"에러 발생: {e}")  # 디버그용
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'url_collection/add_url.html', {'team': {'team_id': team_id}})

def storage_view(request, team_id):
    # 해당 team_id의 URL들을 불러옵니다.
    urls = URLStorage.objects.filter(team_id=str(team_id)).order_by('-created_at')
    
    context = {
        'team': {'team_id': team_id},
        'urls': urls,
    }
    return render(request, 'url_collection/storage.html', context)

def test_page(request):
    """
    테스트 페이지를 렌더링하는 뷰입니다.
    """
    return render(request, "url_collection/test.html")