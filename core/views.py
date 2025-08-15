# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from team.models import Team

# 첫 페이지
def index(request):
    return render(request, 'core/index.html')

# 팀 생성 페이지
def create_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        if team_name:
            team = Team.objects.create(team_name=team_name)
            request.session['team_id'] = str(team.team_id)
            return redirect('core:set_deadline')
    return render(request, 'core/create_team.html')

# 마감일 설정 페이지
def set_deadline(request):
    team_id = request.session.get('team_id')
    if not team_id:
        return redirect('core:create_team')

    if request.method == 'POST':
        try:
            team = get_object_or_404(Team, team_id=team_id)
            deadline_date = request.POST.get('deadline_date')
            deadline_time = request.POST.get('deadline_time')
            
            # 디버깅용 로그
            print(f"받은 데이터 - 날짜: {deadline_date}, 시간: {deadline_time}")
            
            if not deadline_date or not deadline_time:
                # 에러 메시지와 함께 다시 폼 표시
                return render(request, 'core/set_deadline.html', {
                    'error': '날짜와 시간을 모두 입력해주세요.'
                })

            team.deadline_date = deadline_date
            team.deadline_time = deadline_time
            team.save()

            return redirect('core:main_page', team_id=team_id)
        except Team.DoesNotExist:
            return redirect('core:create_team')
        except Exception as e:
            print(f"오류 발생: {e}")
            return render(request, 'core/set_deadline.html', {
                'error': '저장 중 오류가 발생했습니다.'
            })

    return render(request, 'core/set_deadline.html')

# 메인 페이지
def main_page(request, team_id):
    try:
        team = get_object_or_404(Team, team_id=team_id)
    except:
        return redirect('core:index')

    context = {
        'team': team
    }
    return render(request, 'team/main_page.html', context)