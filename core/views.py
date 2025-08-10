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
            # 팀명이 정상적으로 입력되면 다음 페이지로 리다이렉트합니다.
            return redirect('set_deadline')
    
    # GET 요청이거나 폼 데이터가 유효하지 않을 경우, 페이지를 다시 렌더링합니다.
    return render(request, 'core/create_team.html')

# 팀플 기간 설정 페이지를 렌더링하고, POST 요청 시 마감일을 처리하는 뷰 함수입니다.
def set_deadline(request):
    if request.method == 'POST':
        # 세션에서 team_id를 가져옵니다.
        team_id = request.session.get('team_id')
        if team_id:
            try:
                team = Team.objects.get(team_id=team_id)
                deadline_date = request.POST.get('deadline_date')
                deadline_time = request.POST.get('deadline_time')

                # 팀 객체에 마감일과 시간을 저장합니다.
                team.deadline_date = deadline_date
                team.deadline_time = deadline_time
                team.save()

                # 데이터 저장이 완료되면 메인 페이지로 리다이렉트합니다.
                # 아직 메인 페이지가 없으므로 임시로 'index' 페이지로 리다이렉트합니다.
                return redirect('index') 
            except Team.DoesNotExist:
                # 팀 객체가 없는 경우 에러 처리
                return redirect('index') 
    
    return render(request, 'core/set_deadline.html')

# 임시로 메인 페이지를 렌더링하는 뷰 함수입니다.
# 메인 페이지 프론트엔드 작업이 완료되면 이 함수를 보강할 예정입니다.
def main_page(request, team_id):
    return render(request, 'team/main_page.html')