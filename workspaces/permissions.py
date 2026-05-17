from django.http import Http404
from .models import WorkspaceMembership


class WorkspacePermissionMixin:

    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):

        workspace = self.get_workspace()

        try:
            membership = WorkspaceMembership.objects.get(
                user=request.user,
                workspace=workspace
            )
        except WorkspaceMembership.DoesNotExist:
            raise Http404

        if self.allowed_roles and membership.role not in self.allowed_roles:
            raise Http404

        return super().dispatch(request, *args, **kwargs)
    
