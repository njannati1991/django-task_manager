from django.http import Http404
from .models import WorkspaceMember


class WorkspacePermissionMixin:

    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):

        workspace = self.get_workspace()

        try:
            membership = WorkspaceMember.objects.get(
                members=request.user,
                workspace=workspace
            )
        except WorkspaceMember.DoesNotExist:
            raise Http404

        if self.allowed_roles and membership.role not in self.allowed_roles:
            print(self.allowed_roles)
            print(membership.role)
            raise Http404

        return super().dispatch(request, *args, **kwargs)
    
