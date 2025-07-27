# MyTeamPlanner/myteam_planner/team/views.py

from django.shortcuts import render, get_object_or_404
from .models import Team # 현재 앱의 Team 모델 임포트
# from team.models import Team # (만약 team 앱 내에서 Team 모델을 참조할 경우)

# 메인 페이지
def main_page_view(request, team_token):
    # team_token을 사용하여 해당 팀 객체를 가져옵니다.
    team = get_object_or_404(Team, unique_url_token=team_token)

    # progress_bar 계산 (예시: 팀 생성 후 10일 지났으면 10/팀플기간 * 100%)
    # 실제로는 기간 설정이 완료된 후에 계산하는 것이 더 정확합니다.
    progress = 0
    if team.team_period_start and team.team_period_end:
        total_duration = (team.team_period_end - team.team_period_start).days
        if total_duration > 0:
            elapsed_duration = (datetime.now() - team.team_period_start).days
            progress = max(0, min(100, (elapsed_duration / total_duration) * 100))
    else:
        progress = 0 # 기간이 설정되지 않았으면 0%

    context = {
        'team_name': team.team_name,
        'team_token': team_token,
        'progress': round(progress), # 소수점 없이 정수로 표시
    }
    return render(request, 'team/main_page.html', context)