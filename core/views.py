from django.shortcuts import render, redirect
from team.models import Team # Team 모델을 import 합니다.

# 첫 페이지(시작 페이지)를 렌더링하는 뷰 함수입니다.
def index(request):
    return render(request, 'core/index.html')

# 팀명 입력 페이지를 렌더링하고, POST 요청 시 팀명을 처리하는 뷰 함수입니다.
def create_team(request):
    if request.method == 'POST':
        # POST 요청일 경우, 폼에서 팀명 데이터를 가져옵니다.
        team_name = request.POST.get('team_name')
        if team_name:
            # 새로운 Team 객체를 생성하고 저장합니다.
            team = Team.objects.create(team_name=team_name)
            # 생성된 팀의 고유 ID를 세션에 저장하여 다음 페이지로 전달합니다.
            request.session['team_id'] = str(team.team_id)
            # 'set_deadline' 페이지로 이동합니다.
            return redirect('set_deadline')
    
    # GET 요청이거나 폼 데이터가 유효하지 않을 경우, 페이지를 다시 렌더링합니다.
    return render(request, 'core/create_team.html')

# 팀플 기간 설정 페이지를 렌더링하고, POST 요청 시 마감일을 처리하는 뷰 함수입니다.
def set_deadline(request):
    # 세션에서 team_id를 먼저 확인합니다.
    team_id = request.session.get('team_id')
    if not team_id:
        # team_id가 없으면 팀 생성 페이지로 리다이렉트하여 세션을 다시 설정하도록 유도
        return redirect('create_team')

    if request.method == 'POST':
        try:
            team = Team.objects.get(team_id=team_id)
            deadline_date = request.POST.get('deadline_date')
            deadline_time = request.POST.get('deadline_time')

            # 팀 객체에 마감일과 시간을 저장합니다.
            team.deadline_date = deadline_date
            team.deadline_time = deadline_time
            team.save()

            # 데이터 저장이 완료되면 메인 페이지로 리다이렉트합니다.
            # team_id를 URL 인자로 전달합니다.
            return redirect('main_page', team_id=team_id) 
        except Team.DoesNotExist:
            # 팀 객체가 없는 경우 에러 처리
            return redirect('create_team') 
    
    return render(request, 'core/set_deadline.html')

# 메인 페이지를 렌더링하는 뷰 함수입니다.
def main_page(request, team_id):
    # URL에서 받은 team_id로 팀 정보를 조회합니다.
    try:
        team = Team.objects.get(team_id=team_id)
    except Team.DoesNotExist:
        # 팀이 존재하지 않으면 첫 페이지로 리다이렉트합니다.
        return redirect('index')
    
    # 템플릿에 전달할 컨텍스트(context)를 만듭니다.
    context = {
        'team_name': team.team_name,
    }
    return render(request, 'team/main_page.html', context)