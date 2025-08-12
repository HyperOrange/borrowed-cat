from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from team.models import Team
from .models import TodoItem

def todo_list_page(request, team_id):
    team = get_object_or_404(Team, team_id=team_id)
    todos = TodoItem.objects.filter(team=team).order_by('due_date')

    context = {
        'team_id': team.team_id,
        'todos': todos,
    }
    return render(request, 'todo_list/todo_list_page.html', context)

def todo_add_page(request, team_id):
    team = get_object_or_404(Team, team_id=team_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        assignee = request.POST.get('assignee_id') # 나중에 멤버 ID로 변경 예정
        priority = request.POST.get('priority')
        description = request.POST.get('description')

        TodoItem.objects.create(
            team=team,
            title=title,
            due_date=due_date,
            assignee=assignee,
            priority=priority,
            description=description,
        )
        return redirect('todo_list:list', team_id=team_id)

    context = {
        'team_id': team.team_id,
    }
    return render(request, 'todo_list/todo_add_page.html', context)