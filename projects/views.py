from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.http import Http404
from django.urls import reverse

from workspaces.models import Workspace
from .forms import ProjectCreateForm
from .models import Project




class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = 'projects/project_create.html'

    def dispatch(self, request, *args, **kwargs):

        self.workspace = Workspace.objects.filter(id=self.kwargs['workspace_id'], members=request.user).first()

        if not self.workspace:
            raise Http404('Workspace not found.')

        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):

        form.instance.workspace = self.workspace

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('workspace-detail', kwargs={'pk': self.workspace.pk})
    

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.select_related(
            'workspace'
        ).prefetch_related(
                'tasks'
            ).filter(
                    workspace__members = self.request.user
                )
