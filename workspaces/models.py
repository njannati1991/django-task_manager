from django.db import models
# from django.conf import settings
from django.contrib.auth import get_user_model
from core.models import BaseModel


User = get_user_model()


class Workspace(BaseModel):


    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_workspaces')
    

    def __str__(self):
        return self.name
    


class WorkspaceMember(BaseModel):

    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"
        VIEWER = "viewer", "Viewer"

    members = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspaces')

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="memberships")

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("members", "workspace")

    def __str__(self):
        return f"{self.members.username} - {self.workspace} ({self.role})"




