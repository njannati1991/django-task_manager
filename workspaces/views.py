from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from workspaces.models import Workspace

class WorkspaceListView(LoginRequiredMixin, ListView):
    model = Workspace
    context_object_name = 'workspaces'
    template_name = 'workspaces/workspace_list.html'


    def get_queryset(self):
        return Workspace.objects.filter(members = self.request.user)
    

class WorkspaceDetailView(DetailView):
    model = Workspace
    template_name = 'workspaces/workspace_detail.html'
    context_object_name = 'workspace'
    



class WorkspaceCreateView(LoginRequiredMixin, CreateView):
    model = Workspace
    fields = ['name']
    context_object_name = 'workspace'
    template_name = 'workspaces/workspace_create.html'
    success_url = reverse_lazy('workspace-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.members.add(self.request.user)
        response = super().form_valid(form)
        

        return response