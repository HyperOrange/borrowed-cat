import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class Team(models.Model):
    # 팀플 관리 페이지의 고유 URL에 사용될 ID입니다.
    # UUID를 사용해 중복 없는 고유한 값을 자동으로 생성합니다.
    team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # 사용자가 입력한 팀명을 저장하는 필드입니다.
    team_name = models.CharField(max_length=100)

    # 팀플 마감일을 저장하는 필드입니다.
    deadline_date = models.DateField(null=True, blank=True)
    
    # 팀플 마감 시간을 저장하는 필드입니다.
    deadline_time = models.TimeField(null=True, blank=True)

    # Django Admin 등에서 객체를 표시할 때 팀명으로 보여주도록 설정합니다.
    def __str__(self):
        return self.team_name

class TeamMember(models.Model):
    # 이 멤버가 속한 팀을 외래 키로 연결합니다.
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    
    # 팀원의 닉네임
    nickname = models.CharField(max_length=50)

    # 선택한 고양이 프로필 이미지 파일명
    profile_image = models.CharField(max_length=100, default='cat_1.jpg')

    # 선택한 수식어들을 콤마로 구분하여 저장합니다.
    tags = models.CharField(max_length=255, blank=True, null=True)

    # Django Admin 등에서 객체를 표시할 때 닉네임으로 보여주도록 설정합니다.
    def __str__(self):
        return f"{self.nickname} ({self.team.team_name})"