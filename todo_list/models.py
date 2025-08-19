# todo_list/models.py
from django.db import models
<<<<<<< Updated upstream
from team.models import Team, TeamMember

class ToDoItem(models.Model):
    PRIORITY_CHOICES = [
        ("L", "Low"),
        ("M", "Medium"),
        ("H", "High"),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="todos")
    assignee = models.ForeignKey(
        TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="todos"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default="M")
    is_completed = models.BooleanField(default=False)

=======
from django.utils import timezone

class ToDoItem(models.Model):
    team = models.ForeignKey("team.Team", on_delete=models.CASCADE, related_name="todos")
    title = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    due_at = models.DateTimeField(null=True, blank=True)  # 마감일(시간 선택 가능)
    assignee = models.ForeignKey(
        "team.TeamMember",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="todos"
    )
    is_done = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        "team.TeamMember",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="created_todos"
    )
>>>>>>> Stashed changes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
<<<<<<< Updated upstream
        ordering = ["is_completed", "due_date", "-priority", "-created_at"]

    def __str__(self):
        return f"[{self.team}] {self.title}"

=======
        ordering = ["is_done", "due_at", "-id"]

    def __str__(self):
        return f"[{self.team_id}] {self.title}"

    @property
    def dday(self):
        """템플릿에서 D-DAY 표기용"""
        if not self.due_at:
            return ""
        today = timezone.localdate()
        due = timezone.localtime(self.due_at).date()
        delta = (due - today).days
        if delta > 0:
            return f"D - {delta}"
        elif delta == 0:
            return "D - DAY"
        else:
            return f"D + {abs(delta)}"
>>>>>>> Stashed changes
