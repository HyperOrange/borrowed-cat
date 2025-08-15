# todo_list/views.py
from django.shortcuts import render, redirect, get_object_or_404
from team.models import Team

def list(request, team_id):
    try:
        team = Team.objects.get(team_id=team_id)
    except Team.DoesNotExist:
        return redirect('core:index')

    context = {
        'team': team,
        'team_id': team_id
    }
    return render(request, 'todo_list/todo_list_page.html', context)

def new(request, team_id):
    try:
        team = Team.objects.get(team_id=team_id)
    except Team.DoesNotExist:
        return redirect('core:index')

    if request.method == 'POST':
        # 여기에 새 할 일 저장 로직 추가
        return redirect('todo_list:list', team_id=team_id)

    return render(request, 'todo_list/todo_new.html', {'team': team, 'team_id': team_id})