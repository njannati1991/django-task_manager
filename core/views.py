from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from invitation.models import WorkspaceInvitation
from workspaces.models import Workspace
from projects.models import Project




User = get_user_model()

class HomeView(TemplateView):
    template_name = 'core/home.html'


class AdminDashboard(TemplateView):
    template_name = 'core/admin_dashboard.html'


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/user_dashboard.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['workspaces'] = Workspace.user_workspace_list(self.request.user)
        data['total_projects'] = Project.user_total_projects(self.request.user)
        data['total_members'] = User.objects.filter(
            memberships__workspace__in = data['workspaces'].values_list('id', flat=True)
        ).distinct().count()
        data['pendig_invite'] = WorkspaceInvitation.objects.filter(invited_by=self.request.user).count()

        return data
    



class EditPageView(LoginRequiredMixin, TemplateView):
    template_name = 'core/edit_page.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['workspaces'] = Workspace.user_workspace_list(self.request.user).filter(owner=self.request.user)

        return data
    
class DeletePageView(LoginRequiredMixin, TemplateView):
    template_name = 'core/delete_page.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['workspaces'] = Workspace.user_workspace_list(self.request.user).filter(owner = self.request.user)

        return data