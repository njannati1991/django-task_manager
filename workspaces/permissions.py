from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Workspace, WorkspaceMember


class WorkspacePermissionMixin:

    allowed_roles = []


    def get_workspace(self):

        workspace_id = self.kwargs.get('workspace_pk') or self.kwargs.get('workspace_id') or self.kwargs.get('pk')
        return get_object_or_404(Workspace, id=workspace_id)
 
    def dispatch(self, request, *args, **kwargs):

        self.workspace = self.get_workspace()

        try:
            membership = WorkspaceMember.objects.get(
                member=request.user,
                workspace=self.workspace
            )
        except WorkspaceMember.DoesNotExist:
            raise Http404

        if self.allowed_roles and membership.role not in self.allowed_roles:
            print(self.allowed_roles)
            print(membership.role)
            raise Http404

        return super().dispatch(request, *args, **kwargs)
    
