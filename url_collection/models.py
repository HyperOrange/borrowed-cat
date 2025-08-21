# myteam_planner/url_collection/models.py

from django.db import models
from team.models import Team # Team 모델 임포트

class Link(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='links')
    url = models.URLField()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title