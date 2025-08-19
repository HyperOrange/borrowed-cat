# role_distribution/models.py
from django.db import models
from team.models import Team, TeamMember

class Role(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='roles')
    role_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.team.team_name} - {self.role_name}'

class RoleAssignment(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='assignments')
    member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='assigned_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='assigned_to')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'role')

    def __str__(self):
        return f'{self.member.nickname} - {self.role.role_name}'