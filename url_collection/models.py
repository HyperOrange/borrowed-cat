from django.db import models

class URLStorage(models.Model):
    team_id = models.CharField(max_length=100)  # UUID를 문자열로 저장
    url = models.URLField()
    title = models.CharField(max_length=200, blank=True)
    favicon_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Team {self.team_id} - {self.url}"