# MyTeamPlanner/myteam_planner/core/views.py

from django.shortcuts import render, redirect
from team.models import Team # team 앱의 Team 모델 임포트
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt # CSRF 보호 비활성화 (개발용, 배포 시 제거 또는 적절히 처리)

# 첫 페이지 (시작하기 버튼)
def index_view(request):
    return render(request, 'core/index.html')

# 팀명 입력 및 처리 페이지 (Activity Views)
@csrf_exempt # 임시로 CSRF 보호 비활성화 (보안 취약점, 나중에 Form 활용 시 제거)
def create_team_view(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name') # 'team_name' 이라는 이름의 input에서 값 가져오기

        if team_name:
            # Team 모델에 새로운 팀 생성 및 저장
            new_team = Team.objects.create(team_name=team_name)
            # 팀 생성 후, 팀플 기간 설정 페이지로 리다이렉트
            # 'set_period'는 set_period_view에 연결될 URL 패턴의 이름 (뒤에서 정의)
            return redirect(reverse('set_period', kwargs={'team_token': new_team.unique_url_token}))
        else:
            # 팀명이 입력되지 않았을 경우, 에러 메시지와 함께 다시 렌더링
            return render(request, 'core/create_team.html', {'error': '팀명을 입력해주세요.'})
    
    # GET 요청 (시작하기 버튼 누른 후 처음 진입 시)
    return render(request, 'core/create_team.html')

# 팀플 설정 기간 페이지 (간단하게만 구현)
def set_period_view(request, team_token):
    # team_token을 사용하여 해당 팀 객체를 가져올 수 있습니다.
    # 하지만 이 단계에서는 단순히 페이지를 렌더링만 합니다.
    # 실제 구현에서는 여기서 달력 API 연동 및 기간 저장 로직이 추가됩니다.
    return render(request, 'team/set_period.html', {'team_token': team_token})