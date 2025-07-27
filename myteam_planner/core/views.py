# MyTeamPlanner/myteam_planner/core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from team.models import Team
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse # JsonResponse, HttpResponse 임포트
from datetime import datetime
import json # JSON 데이터 파싱을 위해 임포트

# 첫 페이지 (시작하기 버튼 및 모달 포함)
def index_view(request):
    return render(request, 'core/index.html')

# 팀명 입력 처리 (AJAX 요청 처리)
# 이제 이 뷰는 HTTP POST 요청만 받고, JSON 응답을 보냅니다.
@csrf_exempt # 임시로 CSRF 보호 비활성화 (보안 취약점, 배포 시 Form 사용 및 제거)
def create_team_ajax_view(request):
    if request.method == 'POST':
        try:
            # 클라이언트에서 JSON 형식으로 데이터를 보낼 것이므로, request.body에서 파싱
            data = json.loads(request.body)
            team_name = data.get('team_name')

            if team_name:
                new_team = Team.objects.create(team_name=team_name)
                # 성공 시, 생성된 팀의 메인 페이지 URL을 반환
                main_page_url = reverse('set_period', kwargs={'team_token': new_team.unique_url_token})
                return JsonResponse({'status': 'success', 'redirect_url': main_page_url})
            else:
                return JsonResponse({'status': 'error', 'message': '팀명을 입력해주세요.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    # GET 요청은 허용하지 않음 (이 뷰는 AJAX POST 전용)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


# 팀플 설정 기간 페이지 (이전과 동일)
@csrf_exempt
def set_period_view(request, team_token):
    team = get_object_or_404(Team, unique_url_token=team_token)

    if request.method == 'POST':
        try:
            start_date_str = request.POST.get('start_date')
            start_time_str = request.POST.get('start_time')
            end_date_str = request.POST.get('end_date')
            end_time_str = request.POST.get('end_time')

            start_datetime_str = f"{start_date_str} {start_time_str}"
            end_datetime_str = f"{end_date_str} {end_time_str}"

            team.team_period_start = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
            team.team_period_end = datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M")
            team.save()

            return redirect(reverse('main_page', kwargs={'team_token': team.unique_url_token}))

        except (ValueError, TypeError):
            return render(request, 'team/set_period.html', {
                'team_token': team_token,
                'error': '날짜와 시간을 올바르게 입력해주세요.'
            })
    
    return render(request, 'team/set_period.html', {'team_token': team_token})