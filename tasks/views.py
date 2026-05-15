from django.shortcuts import render
from django.views.generic import CreateView
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