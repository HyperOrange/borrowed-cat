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
    # 변경: 한 명에게 여러 역할이 할당될 수 있으므로, 딕셔너리가 아닌 리스트로 그룹화합니다.
    assignments = RoleAssignment.objects.filter(team=team).select_related('member', 'role')
    member_roles = {}
    for assignment in assignments:
        if assignment.member.id not in member_roles:
            member_roles[assignment.member.id] = []
        member_roles[assignment.member.id].append(assignment.role.name)
    
    # 팀원 목록을 순회하며 역할 정보를 추가
    members_with_roles = []
    for member in TeamMember.objects.filter(team=team).order_by('nickname'):
        members_with_roles.append({
            'id': member.id,
            'nickname': member.nickname,
            'profile_image': member.profile_image,
            # 변경: 한 명에게 여러 역할이 할당될 수 있으므로, 리스트로 역할을 전달합니다.
            'roles': member_roles.get(member.id, [])
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


                # 전체 배정일 경우 기존 할당을 모두 삭제
                if target_scope == '전체':
                    RoleAssignment.objects.filter(team=team, member__in=members_to_assign).delete()
                else: # 미정자만 배정일 경우 기존 할당을 삭제하지 않음
                    RoleAssignment.objects.filter(team=team, member__in=members_to_assign).delete()
                
                final_roles = []
                for role_name in selected_roles:
                    role, created = Role.objects.get_or_create(name=role_name)
                    final_roles.append(role)
                
                assignments_to_create = []
                
                if allow_duplicates:
                    # 변경: 역할 수가 팀원 수보다 적을 때도 모든 역할을 분배하도록 로직을 개선
                    if len(final_roles) > 0:
                        # 역할 리스트를 충분히 늘려 모든 팀원이 역할을 받도록 함
                        role_list_for_random = final_roles * (len(members_to_assign) // len(final_roles) + 1)
                        random.shuffle(role_list_for_random)
                        
                        # 각 팀원에게 역할을 할당
                        for member in members_to_assign:
                            if role_list_for_random:
                                assigned_role = role_list_for_random.pop()
                                assignments_to_create.append(RoleAssignment(team=team, member=member, role=assigned_role))

                else: # 역할 중복 허용 안함
                    if len(members_to_assign) > len(final_roles):
                        return JsonResponse({'success': False, 'message': '팀원 수보다 역할 수가 적습니다. 중복 허용 옵션을 선택하거나 역할을 더 추가해주세요.'})
                    
                    random.shuffle(members_to_assign)
                    random.shuffle(final_roles)


                    for member, role in zip(members_to_assign, final_roles):
                        assignments_to_create.append(RoleAssignment(team=team, member=member, role=role))
            
            RoleAssignment.objects.bulk_create(assignments_to_create)


            updated_assignments = RoleAssignment.objects.filter(team=team).select_related('member', 'role')
            # 변경: 프론트엔드로 여러 역할 정보를 전달하기 위해 데이터 구조를 변경
            updated_assignments_by_member = {}
            for a in updated_assignments:
                if a.member.id not in updated_assignments_by_member:
                    updated_assignments_by_member[a.member.id] = []
                updated_assignments_by_member[a.member.id].append(a.role.name)

            result_data = {
                'success': True,
                'message': '역할 배정이 완료되었습니다!',
                'assignments': updated_assignments_by_member
            }
            return JsonResponse(result_data)


        except Exception as e:
            return JsonResponse({'success': False, 'message': f'오류 발생: {e}'}, status=400)
    
    return JsonResponse({'success': False, 'message': '잘못된 접근입니다.'}, status=405)


# 변경: 개별 팀원에게 역할 할당을 처리하는 새로운 API 뷰를 추가
def assign_single_role(request, team_id):
    if request.method == 'POST':
        try:
            team = get_object_or_404(Team, team_id=team_id)
            member_id = request.POST.get('member_id')
            role_name = request.POST.get('role_name')

            member = get_object_or_404(TeamMember, id=member_id)
            role, created = Role.objects.get_or_create(name=role_name)

            with transaction.atomic():
                # 기존 할당을 모두 삭제하고 새 역할을 할당합니다.
                RoleAssignment.objects.filter(team=team, member=member).delete()
                assignment = RoleAssignment.objects.create(team=team, member=member, role=role)

            return JsonResponse({
                'success': True, 
                'message': '역할이 성공적으로 할당되었습니다.',
                'member_id': member.id,
                'role_name': assignment.role.name
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'오류 발생: {e}'}, status=400)
    
    return JsonResponse({'success': False, 'message': '잘못된 접근입니다.'}, status=405)

# 아래는 새로운 import
import requests
import json
import base64

# Gemini API의 엔드포인트와 키를 상수로 정의합니다.
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key="
API_KEY = "" # API 키는 별도로 설정해야 합니다.


# 변경: AI 기반 역할 배정 API 뷰를 추가
def ai_assign_roles(request, team_id):
    if request.method == 'POST':
        try:
            team = get_object_or_404(Team, team_id=team_id)
            
            # 클라이언트에서 보낸 키워드 데이터를 파싱합니다.
            data = json.loads(request.body)
            team_members_data = data.get('team_members_data', [])

            if not team_members_data:
                return JsonResponse({'success': False, 'message': '팀원 키워드 데이터가 없습니다.'})

            # AI에 보낼 프롬프트 생성
            prompt = "다음 팀원들의 키워드를 분석하여 각각에게 가장 어울리는 역할을 한 가지씩 추천해줘. 역할은 '발표', '자료정리', '자료조사', '발표자료 제작', '백피피티 제작', '보고서 작성', '팀장' 중에서 선택해. 응답은 JSON 형식으로 부탁해. 예시: [{'member_id': 'uuid', 'role': '역할이름'}]"
            
            for member in team_members_data:
                prompt += f"\n- {member['nickname']}의 키워드: {member['keywords']}"
            
            # API 호출을 위한 페이로드 구성
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "responseMimeType": "application/json"
                }
            }

            headers = {
                "Content-Type": "application/json"
            }

            # API 호출
            response = requests.post(f"{API_URL}{API_KEY}", headers=headers, data=json.dumps(payload))
            response.raise_for_status() # HTTP 오류가 발생하면 예외를 발생시킵니다.
            
            ai_assignments = response.json().get('candidates')[0]['content']['parts'][0]['text']
            ai_assignments = json.loads(ai_assignments)

            with transaction.atomic():
                # 기존 할당을 모두 삭제합니다.
                member_ids = [member['id'] for member in team_members_data]
                RoleAssignment.objects.filter(team=team, member__id__in=member_ids).delete()

                # AI가 제안한 역할로 할당을 생성합니다.
                assignments_to_create = []
                for assignment in ai_assignments:
                    member = get_object_or_404(TeamMember, nickname=assignment['member_id'])  # member_id 값이 닉네임인 경우
                    role, created = Role.objects.get_or_create(name=assignment['role'])
                    assignments_to_create.append(RoleAssignment(team=team, member=member, role=role))
                
                RoleAssignment.objects.bulk_create(assignments_to_create)

            updated_assignments = RoleAssignment.objects.filter(team=team).select_related('member', 'role')
            updated_assignments_by_member = {}
            for a in updated_assignments:
                if a.member.id not in updated_assignments_by_member:
                    updated_assignments_by_member[a.member.id] = []
                updated_assignments_by_member[a.member.id].append(a.role.name)

            return JsonResponse({
                'success': True,
                'message': 'AI가 역할 배정을 완료했습니다!',
                'assignments': updated_assignments_by_member
            })

        except requests.RequestException as e:
            return JsonResponse({'success': False, 'message': f'API 호출 중 오류 발생: {e}'}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'API 응답 형식이 올바르지 않습니다.'}, status=500)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'오류 발생: {e}'}, status=400)
    
    return JsonResponse({'success': False, 'message': '잘못된 접근입니다.'}, status=405)