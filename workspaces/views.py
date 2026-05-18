from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, ListView, DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Prefetch, Q

from workspaces.models import Workspace, WorkspaceMember
from .permissions import WorkspacePermissionMixin
from .forms import AddMemberForm, UpdateMemberForm


User = get_user_model()

class WorkspaceListView(LoginRequiredMixin, ListView):
    model = Workspace
    context_object_name = 'workspaces'
    template_name = 'workspaces/workspace_list.html'


    def get_queryset(self):
        user = self.request.user

        user_memberships = WorkspaceMember.objects.filter(members=user).select_related('workspace')

        return (
            Workspace.objects.filter(
                Q(owner=user) |
                Q(memberships__members=user)
            )
            .prefetch_related(
                Prefetch('memberships', queryset=user_memberships, to_attr='user_membership')
            )
            .distinct()
        )
    
    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     data['role'] = WorkspaceMember.objects.filter(
    #         members = self.request.user,
    #         Workspace = self.kwargs['workspace']
    #     ).values('role')
    #     return data
    

class WorkspaceDetailView(LoginRequiredMixin, DetailView):
    model = Workspace
    template_name = 'workspaces/workspace_detail.html'
    context_object_name = 'workspace'


    def get_queryset(self):
        return Workspace.objects.prefetch_related(
            'projects',
            Prefetch(
                'memberships', queryset=WorkspaceMember.objects.filter(is_active=True),
            )
        )



class WorkspaceCreateView(LoginRequiredMixin, CreateView):

    model = Workspace
    fields = ['name']
    context_object_name = 'workspace'
    template_name = 'workspaces/workspace_create.html'
    success_url = reverse_lazy('workspace-list')

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.owner = self.request.user
            self.object = form.save()

            WorkspaceMember.objects.create(
                members = self.object.owner,
                workspace = self.object,
                role = 'owner',
            )
        
        response = super().form_valid(form)

        return response
    

    
    

class AddMemberView(LoginRequiredMixin, WorkspacePermissionMixin, FormView):
    
    template_name = 'workspaces/add_member.html'
    form_class = AddMemberForm
    
    
    allowed_roles = ['owner', 'admin']

    # def get_workspace(self):
    #     return get_object_or_404(Workspace, id=self.kwargs['workspace_pk'])


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['workspace'] = self.get_workspace()
        return kwargs



    def form_valid(self, form):
        role = form.cleaned_data['role']
        user = get_object_or_404(User, username=form.cleaned_data['username'])
        workspace = self.get_workspace()
        WorkspaceMember.objects.create(
            workspace = workspace,
            members = user,
            role = role
        )
        
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['workspace'] = self.get_workspace()

        return data


    def get_success_url(self):
        return reverse('workspace-detail', kwargs={'pk':self.kwargs['workspace_pk']})
    

class DeleteMemberView(LoginRequiredMixin,WorkspacePermissionMixin, DeleteView):

    allowed_roles = ['owner', 'admin']

    model = WorkspaceMember
    
    def get_object(self, queryset = None):
        return get_object_or_404(
            WorkspaceMember,
            workspace__id = self.kwargs['workspace_pk'],
            members__username = self.kwargs['username']
        )
    
    def get_success_url(self):
        return reverse('workspace-detail', kwargs={'pk':self.kwargs['workspace_pk']})


class UpdateMemberView(LoginRequiredMixin, WorkspacePermissionMixin, UpdateView):
    
    
    allowed_roles = ['owner', 'admin']
    model = WorkspaceMember
    form_class = UpdateMemberForm
    template_name = 'workspaces/update_member.html'

    

    def get_object(self, queryset = None):
        return get_object_or_404(
            WorkspaceMember,
            workspace__id = self.kwargs['workspace_pk'],
            members__username = self.kwargs['username']
        )
    
    def get_success_url(self):
        return reverse('workspace-detail', kwargs={'pk':self.kwargs['workspace_pk']})
        
