from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from workspaces.models import Workspace, WorkspaceMember
from .permissions import WorkspacePermissionMixin
from .forms import AddMemberForm

class WorkspaceListView(LoginRequiredMixin, ListView):
    model = Workspace
    context_object_name = 'workspaces'
    template_name = 'workspaces/workspace_list.html'


    def get_queryset(self):
        return Workspace.objects.filter(owner=self.request.user)
    

class WorkspaceDetailView(LoginRequiredMixin, DetailView):
    model = Workspace
    template_name = 'workspaces/workspace_detail.html'
    context_object_name = 'workspace'


    def get_queryset(self):
        return Workspace.objects.prefetch_related('projects')



class WorkspaceCreateView(LoginRequiredMixin, CreateView):

    model = Workspace
    fields = ['name']
    context_object_name = 'workspace'
    template_name = 'workspaces/workspace_create.html'
    success_url = reverse_lazy('workspace-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
      

        return response
    

class AddMemberView(LoginRequiredMixin, WorkspacePermissionMixin, CreateView):

    model = WorkspaceMember
    form_class = AddMemberForm
    template_name = 'workspaces/add_member.html'

    allowed_roles = ['owner', 'admin']

    def get_workspace(self):
        return get_object_or_404(Workspace, id= self.kwargs['workspace_id'])

    def form_valid(self, form):
        
        workspace = self.get_workspace()
        form.instance.workspace = workspace
        
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('workspace-detail', kwargs={'pk': self.kwargs['workspace_id']})