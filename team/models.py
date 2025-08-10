# team/models.py
from django.db import models
import uuid

class Team(models.Model):
    team_name = models.CharField(max_length=100)
    team_period_start = models.DateField(null=True, blank=True)
    team_period_end = models.DateField(null=True, blank=True)
    # 공유용 토큰 (URL에 쓰는 값)
    unique_url_token = models.CharField(max_length=36, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_url_token:
            self.unique_url_token = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team_name}"

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    nickname = models.CharField(max_length=50)
    # 선택: 키워드 문자열 저장. 나중에 JSONField로 바꿔도 됨
    keywords = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.nickname} ({self.team.team_name})"
