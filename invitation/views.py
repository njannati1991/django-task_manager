from django.views.generic import FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from .models import WorkspaceInvitation
from workspaces.models import Workspace, WorkspaceMember
from workspaces.permissions import WorkspacePermissionMixin
from .forms import InviteMemberForm




class InviteMemberView(LoginRequiredMixin, WorkspacePermissionMixin, FormView):

    template_name = 'invitation/invite_member.html'
    form_class = InviteMemberForm

    allowed_roles = ['admin', 'owner']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['workspace'] = self.get_workspace()
        return kwargs

    def form_valid(self, form):
        invitation = form.save(commit=False)
        invitation.workspace = self.workspace
        invitation.invited_by = self.request.user
        invitation.save()

        invite_link = self.request.build_absolute_uri(reverse('register'))

        send_mail(
            subject=f"Invitation to join workspace: {self.workspace.name}",
            message=(
                f"You have been invited to join the workspace '{self.get_workspace().name}'.\n\n"
                f"Your role will be: {invitation.role}\n\n"
                f"Accept invitation:\n{invite_link}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invitation.email],
            fail_silently=False,
        )

        messages.success(self.request, "Invitation sent successfully.")
        return redirect('workspace-detail', self.get_workspace().id)
    
