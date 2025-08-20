# role_distribution/views.py

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from team.models import Team, TeamMember
from .models import Role, RoleAssignment
from django.db import transaction
import random

# 역할 분배 페이지 뷰
def role_distribution_page(request, team_id):
    team = get_object_or_404(Team, team_id=team_id)
    
    # 각 팀원에게 할당된 역할 정보를 가져옵니다.
    assignments = RoleAssignment.objects.filter(team=team).select_related('member', 'role')
    member_roles = {assignment.member.id: assignment.role for assignment in assignments}
    
    # 팀원 목록을 순회하며 역할 정보를 추가
    members_with_roles = []
    for member in TeamMember.objects.filter(team=team).order_by('nickname'):
        members_with_roles.append({
            'id': member.id,
            'nickname': member.nickname,
            'profile_image': member.profile_image,
            'role_name': member_roles.get(member.id).name if member.id in member_roles else "역할 미정"
        })

    # 기본 역할 목록
    predefined_roles = [
        "발표", "자료정리", "자료조사", "발표자료 제작", 
        "백피피티 제작", "보고서 작성", "팀장"
    ]
    
    context = {
        'team': team,
        'members_with_roles': members_with_roles, # <-- 수정된 데이터
        'predefined_roles': predefined_roles,
    }
    return render(request, 'role_distribution/role_distribution_page.html', context)

# 역할 랜덤 배정 API 뷰
def random_assign_roles(request, team_id):
    if request.method == 'POST':
        try:
            team = get_object_or_404(Team, team_id=team_id)
            
            data = request.POST
            target_scope = data.get('target_scope')
            allow_duplicates = data.get('allow_duplicates') == 'true'
            selected_roles = data.getlist('selected_roles')
            new_role = data.get('new_role')

            if new_role:
                selected_roles.append(new_role)

            if not selected_roles:
                return JsonResponse({'success': False, 'message': '선택된 역할이 없습니다.'})

            with transaction.atomic():
                assigned_member_ids = RoleAssignment.objects.filter(team=team).values_list('member__id', flat=True)
                
                if target_scope == '미정자만':
                    members_to_assign = list(TeamMember.objects.filter(team=team).exclude(id__in=assigned_member_ids))
                else: # 전체
                    members_to_assign = list(TeamMember.objects.filter(team=team))
                
                if not members_to_assign:
                    return JsonResponse({'success': False, 'message': '배정할 팀원이 없습니다.'})

                # 기존 역할 초기화 (전체 배정 시)
                if target_scope == '전체':
                    RoleAssignment.objects.filter(team=team).delete()
                
                # 새로운 역할 생성
                final_roles = []
                for role_name in selected_roles:
                    role, created = Role.objects.get_or_create(name=role_name)
                    final_roles.append(role)
                
                assignments_to_create = []
                
                if allow_duplicates:
                    if len(members_to_assign) > 0 and len(final_roles) > 0:
                        role_list_for_random = final_roles * (len(members_to_assign) // len(final_roles) + 1)
                        random.shuffle(role_list_for_random)
                        
                        for member in members_to_assign:
                            if role_list_for_random:
                                assigned_role = role_list_for_random.pop()
                                assignments_to_create.append(RoleAssignment(team=team, member=member, role=assigned_role))
                else:
                    if len(members_to_assign) > len(final_roles):
                        return JsonResponse({'success': False, 'message': '팀원 수보다 역할 수가 적습니다. 중복 허용 옵션을 선택하거나 역할을 더 추가해주세요.'})
                    
                    random.shuffle(members_to_assign)
                    random.shuffle(final_roles)

                    for member, role in zip(members_to_assign, final_roles):
                        assignments_to_create.append(RoleAssignment(team=team, member=member, role=role))
            
            RoleAssignment.objects.bulk_create(assignments_to_create)

            updated_assignments = RoleAssignment.objects.filter(team=team).select_related('member', 'role')
            result_data = {
                'success': True,
                'message': '역할 배정이 완료되었습니다!',
                'assignments': [{
                    'member_id': a.member.id,
                    'role_name': a.role.name,
                } for a in updated_assignments]
            }
            return JsonResponse(result_data)

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'오류 발생: {e}'}, status=400)
    
    return JsonResponse({'success': False, 'message': '잘못된 접근입니다.'}, status=405)