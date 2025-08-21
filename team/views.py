from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, TeamMember
from django.urls import reverse
from django.http import JsonResponse

def add_member(request, team_id):
    team = get_object_or_404(Team, team_id=team_id)
    
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        profile_image = request.POST.get('profile_image')
        tags = request.POST.get('tags')

        if nickname:
            TeamMember.objects.create(
                team=team,
                nickname=nickname,
                profile_image=profile_image,
                tags=tags,
            )
            # 팀원 추가 후 메인 페이지로 리다이렉트
            return redirect(reverse('core:main_page', kwargs={'team_id': team.team_id}))
    
    context = {
        'team_id': team.team_id,
        'is_edit': False,
    }
    return render(request, 'team/profile_settings.html', context)

def edit_member(request, team_id, member_id):
    team = get_object_or_404(Team, team_id=team_id)
    member = get_object_or_404(TeamMember, id=member_id, team=team)
    
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        profile_image = request.POST.get('profile_image')
        tags = request.POST.get('tags')

        if nickname:
            member.nickname = nickname
            member.profile_image = profile_image
            member.tags = tags
            member.save()
            # 수정 후 메인 페이지로 리다이렉트
            return redirect(reverse('core:main_page', kwargs={'team_id': team.team_id}))
    
    context = {
        'team_id': team.team_id,
        'member': member,
        'is_edit': True,
    }
    return render(request, 'team/profile_settings.html', context)

def get_progress_ajax(request, team_id):
    """AJAX로 프로그래스 업데이트를 위한 API 뷰"""
    team = get_object_or_404(Team, team_id=team_id)
    progress = team.get_todo_progress()
    
    return JsonResponse({
        'progress': progress
    })