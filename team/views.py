from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Team, TeamMember

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
            return redirect(reverse('team:main_page', kwargs={'team_id': team.team_id}))
    
    context = {
        'team_id': team.team_id,
    }
    return render(request, 'team/profile_settings.html', context)


# 🔥 팀 메인 페이지 뷰
def main_page(request, team_id):
    team = get_object_or_404(Team, team_id=team_id)
    members = TeamMember.objects.filter(team=team)
    context = {
        'team': team,
        'members': members,
    }
    return render(request, 'team/main_page.html', context)
