from django.shortcuts import render, redirect

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

# 팀플 기간 설정 페이지를 렌더링하는 뷰 함수입니다.
def set_deadline(request):
    return render(request, 'core/set_deadline.html')
