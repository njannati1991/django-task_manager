from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import Http404

from projects.models import Project

from .forms import TaskForm
from .models import Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_create.html'
    form_class = TaskForm

    def dispatch(self, request, *args, **kwargs):
        
        self.project = Project.objects.filter(id=self.kwargs['project_id'], workspace__members=request.user).first()

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
    

class TaskUpdateView(LoginRequiredMixin, UpdateView):

    model = Task
    template_name = 'tasks/task_update.html'
    context_object_name = 'task'
    form_class = TaskForm

    def get_queryset(self):
        return Task.objects.filter(project__workspace__members = self.request.user)


    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.object.project.id})
    

class TaskDeleteView(LoginRequiredMixin,View):

    def post(self, request, pk, *args, **kwarg):
        task = get_object_or_404(Task, pk=pk, project__workspace_members=request.user)

        task.is_active = False
        task.save()
        return redirect('project-detail', pk=task.project.id)
    

    # def get_queryset(self):
    #     return Task.objects.filter(project__workspace__members = self.request.user)

    # def get_success_url(self):
    #     return reverse('project-detail', kwargs={'pk': self.object.project.id})