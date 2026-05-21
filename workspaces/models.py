from django.db import models
# from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from core.models import BaseModel


User = get_user_model()


class Workspace(BaseModel):


    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_workspaces')
    description = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return self.name
    
    @classmethod
    def user_workspace_list(cls, user):
        return cls.objects.filter(memberships__member= user).prefetch_related('memberships')
    


    


class WorkspaceMember(BaseModel):

    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"
        VIEWER = "viewer", "Viewer"

    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="memberships")

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("member", "workspace")

    def __str__(self):
        return f"{self.members.username} - {self.workspace} ({self.role})"




