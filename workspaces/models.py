from django.db import models
# from django.conf import settings
from django.contrib.auth import get_user_model
from core.models import BaseModel


User = get_user_model()


class Workspace(BaseModel):

    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        ADMIN = 'admin', 'Admin'
        MEMBER = 'member', 'Member'
        VIEWER = 'viewer', 'Viewer'

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_workspaces')
    members = models.ManyToManyField(User, related_name='workspaces', blank=True, through='WorkspaceMemberShip')

    def __str__(self):
        return self.name
    


class WorkspaceMembership(BaseModel):

    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"
        VIEWER = "viewer", "Viewer"

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="memberships")

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

    class Meta:
        unique_together = ("user", "workspace")

    def __str__(self):
        return f"{self.user} - {self.workspace} ({self.role})"




