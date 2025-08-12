from django.db import models
from team.models import Team # Team 모델을 가져옵니다.

class TodoItem(models.Model):
    # TodoItem이 속한 팀을 외래 키로 연결합니다.
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='todo_items')

    # 할 일의 제목
    title = models.CharField(max_length=200)

    # 할 일에 대한 상세 설명 (선택 사항)
    description = models.TextField(blank=True, null=True)

    # 할 일의 마감 기한
    due_date = models.DateField(null=True, blank=True)

    # 할 일의 우선순위 (높음, 보통, 낮음)
    PRIORITY_CHOICES = [
        ('H', '높음'),
        ('M', '보통'),
        ('L', '낮음'),
    ]
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')

    # 할 일의 완료 여부
    is_completed = models.BooleanField(default=False)

    # 담당자 (추후 TeamMember 모델과 연결 예정)
    # 현재는 간단하게 담당자 이름을 저장합니다.
    assignee = models.CharField(max_length=50, null=True, blank=True)

    # Django Admin 등에서 객체를 표시할 때 제목으로 보여주도록 설정합니다.
    def __str__(self):
        return self.title