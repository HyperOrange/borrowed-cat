# MyTeamPlanner/myteam_planner/team/models.py

from django.db import models
import uuid # 고유 URL 토큰 생성을 위해 uuid 모듈 임포트

class Team(models.Model):
    team_name = models.CharField(max_length=100)
    # DateField -> DateTimeField로 변경하여 시간까지 저장할 수 있도록 함
    team_period_start = models.DateTimeField(null=True, blank=True)
    team_period_end = models.DateTimeField(null=True, blank=True)
    unique_url_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name

    class Meta:
        db_table = 'team'
        ordering = ['-created_at']