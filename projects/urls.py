from django.urls import path
from .views import (
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectDetailView,
)

urlpatterns = [
    path('workspaces/<int:workspace_id>/projects/create/', ProjectCreateView.as_view(), name='project-create'),
    path('update/workspaces/<int:workspace_id>/projects/<int:project_id>/', ProjectUpdateView.as_view(), name='project-update'),
    path('delete/workspaces/<int:workspace_id>/projects/<int:project_id>/', ProjectDeleteView.as_view(), name='project-delete'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    

]