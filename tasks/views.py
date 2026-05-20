from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import Http404

from projects.models import Project
from workspaces.models import WorkspaceMember
from workspaces.permissions import WorkspacePermissionMixin

from .forms import TaskForm
from .models import Task



class TaskCreateView(LoginRequiredMixin, WorkspacePermissionMixin, CreateView):
    model = Task
    template_name = 'tasks/task_create.html'
    form_class = TaskForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(id=self.kwargs['project_id'], workspace__owner = request.user)
        except Project.DoesNotExist:
            return Http404

        if not self.project:
            raise Http404('Project not found.')
        
        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        
        form.instance.project = self.project
        
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.project.id})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs
    
    def get_workspace(self):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        return project.workspace
    

class TaskDetailView(LoginRequiredMixin, DetailView):
    
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'
    pk_url_kwarg = 'pk'

    def get_object(self):

        user = self.request.user
        task = (
            Task.objects
            .select_related('project__workspace')
            .filter(pk=self.kwargs['pk'])
            .first()
        )
        workspace = task.project.workspace
        


        if workspace.owner == user:
            return task
        

        is_member = WorkspaceMember.objects.filter(
            workspace=workspace,
            members = user,
            is_active = True
        ).exists()

        if is_member:
            return task
        
        raise Http404("You do not have permission to view this task.")

        


class TaskUpdateView(LoginRequiredMixin, UpdateView):

    model = Task
    template_name = 'tasks/task_update.html'
    context_object_name = 'task'
    form_class = TaskForm

    def get_queryset(self):
        return Task.objects.filter(project__workspace__owner = self.request.user)


    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.object.project.id})
    

class TaskDeleteView(LoginRequiredMixin,View):

    def post(self, request, pk, *args, **kwarg):
        task = get_object_or_404(Task, pk=pk, project__workspace__owner=request.user)

        task.is_active = False
        task.save()
        return redirect('project-detail', pk=task.project.id)
    

