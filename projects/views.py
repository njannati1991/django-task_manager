from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.http import Http404
from django.urls import reverse, reverse_lazy

from django.db.models import Prefetch, Q
from django.core.paginator import Paginator

from tasks.models import Task
from workspaces.models import Workspace
from .forms import ProjectCreateForm
from .models import Project
from workspaces.permissions import WorkspacePermissionMixin




class ProjectCreateView(LoginRequiredMixin, WorkspacePermissionMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = 'projects/project_create.html'
    allowed_roles = ["owner", "admin"]

    def dispatch(self, request, *args, **kwargs):

        self.workspace = Workspace.objects.filter(id=self.kwargs['workspace_id'], memberships__members=request.user).first()

        if not self.workspace:
            raise Http404('Workspace not found.')

        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):

        form.instance.workspace = self.workspace

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('workspace-detail', kwargs={'pk': self.workspace.pk})
    

    def get_workspace(self):
        return get_object_or_404(Workspace, id=self.kwargs['workspace_id'])
    


class ProjectUpdateView(LoginRequiredMixin,WorkspacePermissionMixin, UpdateView):
    allowed_roles = ['owner']
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project_update.html'
    fields = ['name', 'descriptions']
    pk_url_kwarg = 'project_id'
    
    def get_success_url(self):
        return reverse_lazy('workspace-detail', kwargs={'pk': self.object.workspace.id})
    


class ProjectDeleteView(LoginRequiredMixin, WorkspacePermissionMixin, DeleteView):
    allowed_roles = ['owner']
    model = Project
    pk_url_kwarg = 'project_id'
    def get_success_url(self):
        return reverse_lazy('workspace-detail', kwargs={'pk': self.object.workspace.id})
    

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    

    def get_queryset(self):
        return Project.objects.select_related(
            'workspace'
        ).prefetch_related(
                Prefetch(
                    'tasks', queryset= Task.objects.filter(is_active=True)
                )
            ).filter(
                    workspace__memberships__members = self.request.user,
                )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = self.object.tasks.filter(is_active= True)

        search_query = self.request.GET.get('search')

        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        assigned_to = self.request.GET.get('assigned_to')


        if search_query:
            tasks = tasks.filter(
                Q(title__icontains = search_query) |
                Q(description__icontains = search_query)
            )

        if status:
            tasks = tasks.filter(status=status)
        
        if priority:
            tasks = tasks.filter(priority=priority)

        if assigned_to:
            tasks = tasks.filter(assigned_to=assigned_to)


        paginator = Paginator(tasks, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['todo_count'] = tasks.filter(status='todo').count()
        context['progress_count'] = tasks.filter(status='in_progress').count()
        context['done_count'] = tasks.filter(status='done').count()
        
        
        
        return context
    

