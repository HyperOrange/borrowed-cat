# role_distribution/models.py
from django.db import models
from team.models import Team, TeamMember  # team 앱의 모델을 가져옵니다.

class Role(models.Model):
    """
    팀플 역할을 정의하는 모델 (예: 발표, 자료조사, 보고서 작성)
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="역할 이름")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "역할"
        verbose_name_plural = "역할"

class RoleAssignment(models.Model):
    """
    팀원에게 할당된 역할을 저장하는 모델
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="팀")
    member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, verbose_name="팀원")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="할당 역할")
    
    class Meta:
        unique_together = ('member', 'role')  # 한 팀원은 같은 역할을 중복해서 맡을 수 없습니다.
        verbose_name = "역할 할당"
        verbose_name_plural = "역할 할당"
        
    def __str__(self):
        return f"{self.member.nickname} - {self.role.name}"