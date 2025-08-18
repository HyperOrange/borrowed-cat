# role_distribution/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from team.models import Team, TeamMember
from .models import Role, RoleAssignment
import json

def role_distribution_page(request, team_id):
    team = get_object_or_404(Team, team_id=team_id)
    
    # 팀원 목록과 할당된 역할을 템플릿으로 전달합니다.
    members_with_roles = []
    for member in team.members.all():
        assigned_roles = [assignment.role.role_name for assignment in member.assigned_roles.all()]
        members_with_roles.append({
            'id': member.id,
            'nickname': member.nickname,
            'profile_image': member.profile_image,
            'tags': member.tags,
            'assigned_roles': assigned_roles,
        })

    # 팀에 등록된 역할 목록을 전달합니다.
    available_roles = [role.role_name for role in team.roles.all()]

    context = {
        'team': team,
        'team_id': team.team_id,
        'members_json': json.dumps(members_with_roles), # JSON 형식으로 직렬화
        'roles_json': json.dumps(available_roles),     # JSON 형식으로 직렬화
    }
    return render(request, 'role_distribution/index.html', context)

def update_role_assignments(request, team_id):
    if request.method == 'POST':
        try:
            team = get_object_or_404(Team, team_id=team_id)
            data = json.loads(request.body)
            member_id = data.get('member_id')
            assigned_roles_names = data.get('assigned_roles', [])
            
            member = get_object_or_404(TeamMember, id=member_id, team=team)
            
            # 기존 역할 할당 삭제
            member.assigned_roles.all().delete()
            
            # 새로운 역할 할당
            for role_name in assigned_roles_names:
                role, created = Role.objects.get_or_create(team=team, role_name=role_name)
                RoleAssignment.objects.create(team=team, member=member, role=role)
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)

def add_new_role(request, team_id):
    if request.method == 'POST':
        try:
            team = get_object_or_404(Team, team_id=team_id)
            data = json.loads(request.body)
            role_name = data.get('role_name')
            
            if not role_name:
                return JsonResponse({'status': 'error', 'message': 'Role name is required'}, status=400)
                
            role, created = Role.objects.get_or_create(team=team, role_name=role_name)
            
            if created:
                return JsonResponse({'status': 'success', 'role_name': role.role_name})
            else:
                return JsonResponse({'status': 'error', 'message': 'Role already exists'}, status=409)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)

def handle_ai_assign(request, team_id):
    if request.method == 'POST':
        try:
            team = get_object_or_404(Team, team_id=team_id)
            
            # 모든 역할 할당을 리셋
            RoleAssignment.objects.filter(team=team).delete()
            
            members = list(team.members.all())
            roles = list(team.roles.all())
            
            if not members or not roles:
                return JsonResponse({'status': 'error', 'message': '팀원 또는 역할이 없습니다.'}, status=400)

            # 간단한 랜덤 분배 로직
            import random
            random.shuffle(members)
            
            for member in members:
                if roles:
                    role_to_assign = roles.pop(0) # 역할을 하나씩 순차적으로 할당
                    RoleAssignment.objects.create(team=team, member=member, role=role_to_assign)
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)