from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, TeamMember
from django.urls import reverse

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
    }
    return render(request, 'team/profile_settings.html', context)