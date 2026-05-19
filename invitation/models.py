import uuid

from django.db import models
from django.contrib.auth import get_user_model

from core.models import BaseModel
from workspaces.models import Workspace, WorkspaceMember


User = get_user_model()

class WorkspaceInvitation(BaseModel):

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='invitations')
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=WorkspaceMember.Role, default=WorkspaceMember.Role.MEMBER)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    is_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('workspace', 'email')

    def __str__(self):
        return f"Invite for {self.email} to {self.workspace.name}"


    



